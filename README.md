<h1><strong>Real-Time Health Data Streaming Pipeline with Kafka and Spark</strong></h1>

<h2><strong>Overview</strong></h2>
This project implements a real-time data streaming pipeline capable of handling data from a system that ingests health metrics such as heart rate and oxygen saturation level from patients' smart watch devices and triggers emergency vehicle dispatch within a certain radius if any health metrics exceed abnormal levels. The data generated mimics real-time APIs that supply this data for analytics.

<h2><strong>Architecture</strong></h2>
The architecture of the pipeline includes the following components:

**Data Ingestion**: Two API endpoints provide health metrics in JSON format.<br>
**Kafka Streams**: Used for ingesting and streaming real-time data.<br>
**PySpark**: Structured streaming to process and transform data.<br>
**Amazon S3**: Storage for processed data in Parquet format.<br>
**AWS Glue**: Crawlers to detect new Parquet files in S3 and update Glue tables.<br>
**Docker**: Containerization for easy deployment.<br>
**AWS EC2**: Deployment environment with a domain pointing to the instance.

<h2><strong>Workflow</strong></h2>

**1. Data Ingestion:** Health Data(such as heart rate, oxygen saturation level) and Vehicle Data (such as dispatch time, vehicle location etc) are ingested in JSON (mimicing an API endpoint) <br>
**2. Data Streaming:** Kafka streams consume the data.
<img src="images/verify-data-sent-to-kafka-stream.png" alt="Example Image" style="width:50%;">

<br>
**3. Data Processing:** PySpark processes the ingested data which is transformed and structured for further analytics.<br>
**4. Data Storage:** Processed data is stored in Amazon S3 as Parquet files<br>
**5. Data Cataloging**

<h2><strong>Getting Started</strong></h2>
To get started with this project you need:
- Intermediate Python Proficiency
- Docker Desktop 
- An AWS Account





<h2><strong>Architecture</strong></h2>
