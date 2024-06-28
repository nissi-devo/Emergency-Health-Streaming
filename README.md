<h1><strong>Real-Time Health Data Streaming Pipeline with Kafka and Spark</strong></h1>

<h2><strong>Overview</strong></h2>
<h3>This project implements a real-time data streaming pipeline capable of handling data from a system that ingests health metrics such as heart rate and oxygen saturation level from patients' smart watch devices and triggers emergency vehicle dispatch within a certain radius if any health metrics exceed abnormal levels. The data generated mimics real-time APIs that supply this data for analytics.</h3>

<h2><strong>Architecture</strong></h2>
<h3></h3>The architecture of the pipeline includes the following components:

**Data Ingestion**: Two API endpoints provide health metrics in JSON format.
**Kafka Streams**: Used for ingesting and streaming real-time data.
**PySpark**: Structured streaming to process and transform data.
**Amazon S3**: Storage for processed data in Parquet format.
**AWS Glue**: Crawlers to detect new Parquet files in S3 and update Glue tables.
**Docker**: Containerization for easy deployment.
**AWS EC2**: Deployment environment with a domain pointing to the instance.</h3>

<h2><strong>Workflow</strong></h2>
<h3>
  **1. Data Ingestion**
</h3>


<h2><strong>Getting Started</strong></h2>
<h3> To get started with this project you need:
- Intermediate Python Proficiency
- Docker Desktop 
- An AWS Account
</h3>




<h2><strong>Architecture</strong></h2>
