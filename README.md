# `kafgres`

Integrating Kafka with PostgreSQL in a DBaaS

## Set up a Kafka Service in `Aiven`

- Go to [Console](https://console.aiven.io/)
- Click on `Create a new service`. And follow the steps.
- Select `Kafka` and `Version Number` in `Select your service` section.
- Select the cloud provide from the list consisting AWS, GCP, MS Azure, DigitalOcean, UpCloud, etc.
- Select a region.
- Select a plan according to your required CPU, RAM, Storage, Backup Capability, Nodes, etc.
- Provide the service a name. Note: The service name cannot be changed later.
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

## Author

- Himel Das

## Acknowledgement

### Credits

 - producer.produce_messages was created by taking help from [here](https://github.com/aiven/kafka-python-fake-data-producer).
