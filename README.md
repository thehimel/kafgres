# `kafgres`

## Description

This application provides the following functionalities:

- Send data stream by a producer to Kafka broker.
- Retrieve data stream through a consumer from Kafka broker.
- Insert the fetched data by the consumer to a PostgreSQL database service.

## Terminologies

- PostgreSQL is a powerful, open source object-relational database system.
  - Source: [www.postgresql.org](https://www.postgresql.org/)
- Apache Kafka is an open-source distributed event streaming platform used by thousands of companies
for high-performance data pipelines, streaming analytics, data integration, and mission-critical applications.
  - Source: [kafka.apache.org](https://kafka.apache.org/)
- Kafka Producer is a client that publishes records to the Kafka cluster.
  - Source: [kafka.apache.org](https://kafka.apache.org/26/javadoc/index.html?org/apache/kafka/clients/producer/KafkaProducer.html)
- Kafka Consumer is a client that consumes records from a Kafka cluster.
  - Source: [kafka.apache.org](https://kafka.apache.org/26/javadoc/index.html?org/apache/kafka/clients/consumer/KafkaConsumer.html)

## System Design
- The producer sends data to Kafka server (broker).
- The consumer retrieves data from Kafka server and inserts data to PostgreSQL server.

## Python Requirement

- Python 3.9 or higher.

## Set up a Service in `Aiven`

Use the following steps to set up a `Kafka` and `PostgreSQL` service in `Aiven`.

- Go to [Console](https://console.aiven.io/)
- Click on `Create a new service`. And follow the steps.
- Choose a service (i.e. `Kafka`, `PostgreSQL`, etc.) and `Version Number` in `Select your service` section.
- Select the cloud provide from the options consisting AWS, GCP, MS Azure, DigitalOcean, UpCloud, etc.
- Select a region.
- Select a plan according to your required CPU, RAM, Storage, Backup Capability, Nodes, etc.
- Provide the service a name. *Note: The service name cannot be changed later.*
- Finally, click on `Create Service`.
- Once the status turns `Running`, the service is ready to use.

### Create a Kafka Topic

- Select the service.
- Click on the `Topics` tab.
- Enter a name.
- Default configuration:
  - `Partitions: 1, Replication: 2, Minimum ISR: 1, Retentions Hours: 168 Hours, Retention Bytes: unlimited,
  Cleanup Policy: delete`.
- Click on `Advanced configuration` to define settings.
- Finally, click on `Add topic`.
- Once the status turns `ACTIVE`, the topic is ready to use.

### Enable Kafka REST API

- Select the service.
- On the `Overview` tab, enable `Kafka REST API (Karapace)`.

##  Get Started

### Install Required System Packages (Linux Only)

- Update the local package index.

```sh
sudo apt-get update
```

- To install `psycopg2` in `Linux` we need to install the following packages.

```sh
sudo apt-get install libpq-dev python-dev python3-dev
```

### Install and Activate Virtual Environment

- Install Python 3.9 or higher.
- Clone the repository with `git clone https://github.com/thehimel/kafgres`
- Go to the directory with `cd kafgres`
- Create a virtual environment.
  - Linux: `python3.9 -m venv venv`
  - Windows: `python -m venv venv`
- Activate the virtual environment.
  - Linux: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`

### Install the Requirements

- Install dev requirements with `pip install -r requirements-dev.txt`.
- Install test requirements with `pip install -r requirements-test.txt`.
- Optional: Install pep8 requirements with `pip install -r requirements-pep8.txt`.

### Define the Environment Variables

#### Set the following environment variables in the system.

- KAFKA_CERT_FOLDER
  - Path to the folder where `ca.pem`, `service.cert`, and `service.key` are stored downloaded from the DBaaS console.
- KAFKA_SERVICE_URI
  - Kafka Service URI consisting of `host[:port]` fetched from DBaaS Console.
- KAFKA_TOPIC_NAME
  - Name of the topic.
- PG_SERVICE_URI
  - PostgreSQL Service URI fetched from DBaaS Console.
- PG_TABLE_NAME
  - PostgreSQL table name (Arbitrary).

##### Tip

- For simplicity create a file `kafgres/.env` with the following content.

```dotenv
KAFKA_CERT_FOLDER=/path/to/cert/folder
KAFKA_SERVICE_URI=host:port
KAFKA_TOPIC_NAME=topic-name
PG_SERVICE_URI=postgres://host:port/db-name?sslmode=require
PG_TABLE_NAME=table-name
```

- **This recommendation is only for testing purpose. Do not push the `.env` file to git.**
- `.env` is included in the `.gitignore` so that this file is not pushed to git repository.

## Run the Application

### Run the Consumer and Producer

- Run consumer in another terminal with `python src/manage.py consumer`.
- Run producer in one terminal with `python src/manage.py producer`.

### Insert Data to PostgreSQL

- Test the insertion that inserts a data from faker with `python src/manage.py insert`.

## Stop the Application

- Press `Ctrl+C` to exit a script.

## Testing

This project uses `pytest` for testing.

- Go to the project directory with `cd kafgres`.
- Run tests with one of the following commands:
  - `pytest src`
  - `pytest`

### Integration Test

- One integration test is added to test the data submission by the producer,
data retrieval by the consumer, data insertion to PostgreSQL server,
and data fetch from PostgreSQL server.

### Happy Path and Sad Path Testing

- Happy paths have been added.
- Sad paths will be added in the future.

## Author

- Himel Das

## Acknowledgement

### Credits

- Producer was created by taking help from [kafka-python-fake-data-producer](https://github.com/aiven/kafka-python-fake-data-producer).
- Consumer was created by taking help from the following sources:
  - [Introduction To How Kafka Works And Implementation Using Python-client](https://dev.to/horiyomi/introduction-to-how-kafka-works-and-implementation-using-python-client-1ejo)
  - [Python Examples for Testing Aiven for Apache Kafka](https://help.aiven.io/en/articles/5343895-python-examples-for-testing-aiven-for-apache-kafka)
- Other Sources:
  - [kafka-python](https://kafka-python.readthedocs.io/en/master/usage.html)
  - [Getting started with Aiven for Apache Kafka](https://help.aiven.io/en/articles/489572-getting-started-with-aiven-for-apache-kafka)
  - [Getting started with Aiven Kafka](https://aiven.io/blog/getting-started-with-aiven-kafka)
  - [Getting started with sqlalchemy](https://riptutorial.com/sqlalchemy)
