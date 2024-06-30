from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, TimestampType, BooleanType, DoubleType


def read_kafka_stream(spark, topic, schema):
    # Read Kafka stream from a topic into Spark using spark streaming
    return (
        spark.readStream
        .format('kafka')  # Specifies that the data source is Kafka
        .option('kafka.bootstrap.servers', 'broker:29092')  # Sets the address of the Kafka broker
        .option('subscribe', topic)  # Subscribes to the specified Kafka topic
        .option('startingOffsets', 'earliest')  # Starts reading from the earliest offset of the topic
        .option("failOnDataLoss", "false")  # Prevents the stream from failing if data is lost or not available
        .load()  # Loads the streaming data from Kafka
        .selectExpr('CAST(value as STRING)')  # Casts the 'value' field from Kafka messages to a string
        .select(from_json(col('value'), schema).alias(
            'data'))  # Parses the JSON string in the 'value' field according to the specified schema and aliases the result as 'data'
        .select('data.*')  # Selects all fields from the 'data' struct, flattening the structure.
        .withWatermark('timestamp', '2 minutes')
    # '2 minutes'): Adds a watermark to the data using the 'timestamp' column, allowing for late data to be processed but limiting how late it can be (2 minutes in this case)
    )


def writeStream(input: DataFrame, checkpointFolder, output):
    # Write structured stream to S3 location
    return (
        input.writeStream
        .format('parquet')  # Specifies that the data will be written in Parquet format
        .option('checkpointLocation', checkpointFolder)  # Sets the directory where Spark will store checkpoint information in S3. Checkpointing is necessary for Spark to recover the state of the stream from where it left off in case of failures,
        .option('path', output)  # Sets the directory where the Parquet files will be saved in S3
        .outputMode('append')  # Specifies that only new rows (new data) should be added to the output directory.
        .start()
    )
def main():
    # Creates a Spark session
    # Specifies the required Spark packages for Kafka, Hadoop AWS, and AWS Java SDK
    spark = SparkSession.builder.appName("EmergencyHealthStreaming") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
                                       "org.apache.hadoop:hadoop-aws:3.3.2,"
                                       "com.amazonaws:aws-java-sdk-bundle:1.11.874") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.auth.IAMInstanceCredentialsProvider") \
        .getOrCreate() #Creates the SparkSession if it does not already exist, or retrieves the existing one if it does

    #Adjust the log level
    spark.sparkContext.setLogLevel('WARN')

    location_schema = StructType([
        StructField("latitude", DoubleType(), nullable=False),
        StructField("longitude", DoubleType(), nullable=False)
    ])

    patientSchema = StructType([
        StructField("id", StringType(), True),
        StructField("patient_id", StringType(), False),
        StructField("heart_rate", IntegerType(), True),
        StructField("oxygen_saturation", DoubleType(), True),
        StructField("vo2_max", DoubleType(), True),
        StructField("location", location_schema, False),
        StructField("emergency_alert", BooleanType(), True),
        StructField("timestamp", TimestampType(), True),
    ])

    emergencySchema = StructType([
        StructField("id", StringType(), True),
        StructField("vehicle_id", StringType(), False),
        StructField("vehicle_type", StringType(), True),
        StructField("vehicle_capacity", StringType(), True),
        StructField("location", location_schema, False),
        StructField("patient_id", StringType(), False),
        StructField("dispatch_time", TimestampType(), True),
        StructField("timestamp", TimestampType(), True)
    ])


    patient_df = read_kafka_stream(spark,'patient_data', patientSchema).alias('patient')
    emergency_df = read_kafka_stream(spark, 'emergency_vehicle_data', emergencySchema).alias('emergency')

    query1 = writeStream(patient_df, 's3a://health-streaming-data/checkpoints/patient_data',
                's3a://health-streaming-data/data/patient_data')
    query2 = writeStream(emergency_df, 's3a://health-streaming-data/checkpoints/emergency_vehicle_data',
                's3a://health-streaming-data/data/emergency_vehicle_data')

    query2.awaitTermination()

if __name__ == "__main__":
    main()