from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructField, StructType, StringType, IntegerType, TimestampType, BooleanType, DoubleType
from config import configuration

def main():
    spark = SparkSession.builder.appName("EmergencyHealthStreaming")\
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
            "org.apache.hadoop:hadoop-aws:3.3.2,"
            "com.amazonaws:aws-java-sdk:1.11.469")\
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
    .config("spark.hadoop.fs.s3a.access.key", configuration.get("AWS_ACCESS_KEY"))\
    .config("spark.hadoop.fs.s3a.secret.key", configuration.get("AWS_SECRET_KEY"))\
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")\
    .getOrCreate()

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
        StructField("oxygen_saturation", IntegerType(), True),
        StructField("vo2_max", IntegerType(), True),
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

    def read_kafka_stream(topic, schema):
        return(
            spark.readStream
            .format('kafka')
            .option('kafka.bootstrap.servers', 'broker:29092')
            .option('subscribe', topic)
            .option('startingOffsets', 'earliest')
            .option("failOnDataLoss", "false")
            .load()
            .selectExpr('CAST(value as STRING)')
            .select(from_json(col('value'), schema).alias('data'))
            .select('data.*')
            .withWatermark('timestamp', '2 minutes')
        )

    def writeStream(input: DataFrame, checkpointFolder, output):
        return(
            input.writeStream
            .format('parquet')
            .option('checkpointLocation', checkpointFolder)
            .option('path', output)
            .outputMode('append')
            .start()
        )

    patient_df = read_kafka_stream('patient_data', patientSchema).alias('patient')
    emergency_df = read_kafka_stream('emergency_vehicle_data', emergencySchema).alias('emergency')

    query1 = writeStream(patient_df, 's3a://health-streaming-data/checkpoints/patient_data',
                's3a://health-streaming-data/data/patient_data')
    query2 = writeStream(emergency_df, 's3a://health-streaming-data/checkpoints/emergency_vehicle_data',
                's3a://health-streaming-data/data/emergency_vehicle_data')

    query2.awaitTermination()



if __name__ == "__main__":
    main()