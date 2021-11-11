# Pub/Sub -> Kafka Connector (Hack Day)

In this hack, we aim to setup a Pub/Sub -> Kafka connector that pulls messages from a Pitt-Google Pub/Sub stream and publishes them to a Kafka topic.

## To Do

- [x] [1. Create a single container that runs the connector alone](#1-run-the-connector-alone)
- [x] [2. Create a cluster that runs a Kafka broker and related services, without the connector](#2-run-confluent-platform-broker-and-related-services-without-connector). We must run a broker in order to actually publish the stream.
- [ ] [3. Add the connector to the cluster running the Kafka broker](#3-add-the-connector-to-the-cluster-running-the-kafka-broker)

By the end of the hack, I (Troy Raen) had completed steps 1 and 2.
Step 3 remains to be done.

## Some Basic Info

The connector ([kafka-connector](https://github.com/GoogleCloudPlatform/pubsub/tree/master/kafka-connector), aka "CloudPubSubConnector") is run by calling a bin file and passing in some configs.
It relies on three config files, listed below.
At this point they are mostly complete, but they may still require modification.

- admin.properties
- ps-connector.properties
- psconnect-worker.properties

We will run the connector in "standalone" mode for simplicity, but there is also a "distributed" mode.

In order to listen to the Pub/Sub stream, one must have access to a Google Cloud project and a credentials file.
I set up a test project set up to facilitate this, and I'm happy to let others use it.
The project ID is `pitt-broker-user-project`.
To obtain credentials, contact me at troy.raen@pitt.edu or @troyraen on lsstc.slack.com.

The Pub/Sub subscription we will pull from is attached to this project, and is named "ztf-loop".
It is a "heartbeat" stream publishing ~1 alert/second.
Each message payload is a byte-for-byte pass through of the original ZTF (Kafka) payload.

### Reference Links:

- [kafka-connector](https://github.com/GoogleCloudPlatform/pubsub/tree/master/kafka-connector) (This is a Kafka Connect connector for Pub/Sub <-> Kafka. aka "CloudPubSubConnector")
    - [Source Connector Configs](https://github.com/GoogleCloudPlatform/pubsub/tree/master/kafka-connector#cloudpubsubconnector-configs) ("source" connector = Pub/Sub source -> Kafka sink)
- [Worker Configuration Properties](https://docs.confluent.io/platform/current/connect/references/allconfigs.html)
    - [Configuring Key and Value Converters](https://docs.confluent.io/home/connect/userguide.html#connect-configuring-converters) (See especially the `ByteArrayConverter`, which passes they bytes directly through with no conversion.)
    - [Producer Configs](https://docs.confluent.io/platform/current/installation/configuration/producer-configs.html#cp-config-producer)
        - [Default Connect Producer properties](https://docs.confluent.io/home/connect/userguide.html#kconnect-producers-and-consumers)
- [Configuring and Running Workers ](https://docs.confluent.io/home/connect/userguide.html#configuring-and-running-workers)
- [Quick Start for Confluent Platform](https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html#quickstart) (run a Kafka broker)

## Usage

Clone this repo and navigate to this directory:
```bash
git clone https://github.com/pitt-crc/broker_workshop.git
cd broker_workshop/pubsub_kafka_connect_hack
```

### 1. Run the connector alone

Use the files `docker-compose-connector.yml` and `Dockerfile` to build and run a single container with Java, Java dev kit, Confluent Platform, and the Pub/Sub-Kafka connector. Then login.

```bash
docker compose -f docker-compose-connector.yml up -d
# enter your container name. it might be slightly different than this
container=pubsub_kafka_connect_hack-connector-1
docker exec -it "$container" bash
```

Run the connector using:

```bash
/usr/bin/connect-standalone \
    /pubsub_kafka/psconnect-worker.properties \
    /pubsub_kafka/ps-connector.properties
```

You should see the connector start, beginning with a log entry similar to:

```bash
INFO Kafka Connect standalone worker initializing ... (org.apache.kafka.connect.cli.ConnectStandalone:69)
```

There is no Kafka broker running, so it cannot publish a stream. But it should get to the point where it tries to connect to the broker, and you should see repeated log entries similar to:

```bash
WARN [AdminClient clientId=adminclient-1] Connection to node -1 (localhost/127.0.0.1:9092) could not be established. Broker may not be available. (org.apache.kafka.clients.NetworkClient:803)
```

### 2. Run Confluent Platform broker and related services (without connector)

```bash
docker compose -f docker-compose-cp-all-in-one.yml up -d
```

This should build and spin up a cluster of 9 containers, including "broker" and "connect"

### 3. Add the connector to the cluster running the Kafka broker

We need to merge what we did in step 1 into step 2.
Here is the anticipated TODO list:

- [ ] update docker-compose-cp-all-in-one.yml to add the following to the "connect" container:
    - [ ] download the connector's jar file
    - [ ] set environment variables
    - [ ] copy in the config files from this local directory

Once this is done, we should be able to run the connector and have it pull messages from the Pub/Sub subscription and publish them to the Kafka topic.
Start the connector by calling the bin file from a command prompt in the "connect" container with the command below.

**BEWARE**: The ztf-loop Pub/Sub subscription may contain a *large* number of backlogged alerts, which will come streaming through the connecter at a high rate.
Don't let the connector run for too long in this state.
Use Control-C to stop the connector.
The Google Cloud project `pitt-broker-user-project` uses a free account, and so the maximum number of Pub/Sub messages it is allowed to pull in a given month is capped (should be a few x10^5 ZTF-sized alerts per month).
To avoid this, we should fast forward the subscription to the current time, so that the connector pulls and publish alerts at the live ztf-loop rate of ~1 alert/second.
Contact Troy Raen to do this (troy.raen@pitt.edu, @troyraen on lsstc.slack.com).

```bash
/bin/connect-standalone \
    /home/appuser/psconnect-worker.properties \
    /home/appuser/ps-connector.properties
```

- [ ] Try to listen to the Kafka stream we're producing. The data in the ztf-loop Pub/Sub stream is a byte-for-byte pass through of the original ZTF stream. The resulting Kafka message payloads should be Avro packets that are readable in standard ways.
- [ ] Debug
