# Pub/Sub -> Kafka Connector (Hack Day)

In this hack, we will setup a Kafka Connect, Pub/Sub -> Kafka connector that pulls messages from a Pitt-Google Pub/Sub stream and publishes them to a Kafka topic.

A Google Cloud Project has already been set up to facilitate this.
The project ID is `pitt-broker-user-project`.
The Pub/Sub subscription we will pull from is `ztf-loop-2`.
You will need credentials to access the Pub/Sub stream. Contact troy.raen@pitt.edu or @troyraen on lsstc.slack.com.

This directory includes some starter files that are based on a connector running in the opposite direction (Kafka -> Pub/Sub). They will need to be modified during this hack.
- admin.properties
- ps-connector.properties (already modified for this hack)
- psconnect-worker.properties


There is also a Dockerfile that will build and run a container with Java, Java dev kit, Confluent Platform, and the Pub/Sub-Kafka connector.
You can clone this repo and run the container with the following:
```bash
git clone https://github.com/pitt-crc/broker_workshop.git
cd broker_workshop/pubsub_kafka_connect_hack

docker-compose up
```

Once the starter files are configured properly, we should be able to start the connector by calling the bin file (from a command prompt in the container):

```bash
/bin/connect-standalone \
    /pubsub_kafka/psconnect-worker.properties \
    /pubsub_kafka/ps-connector.properties
```

Reference Links:
- [kafka-connector](https://github.com/GoogleCloudPlatform/pubsub/tree/master/kafka-connector) (Kafka Connect, Pub/Sub <-> Kafka connector. aka CloudPubSubConnector)
- [CloudPubSubConnector Configs](https://docs.confluent.io/home/connect/userguide.html#connect-configuring-converters)
- [Connect Producers and Consumers](https://docs.confluent.io/home/connect/userguide.html#kconnect-producers-and-consumers) (Default Producer properties and overrides)
- [Configuring and Running Workers ](https://docs.confluent.io/home/connect/userguide.html#configuring-and-running-workers) (Confluent)
- [Worker Configuration Properties](https://docs.confluent.io/platform/current/connect/references/allconfigs.html) (Confluent)
- [Configuring Key and Value Converters](https://docs.confluent.io/home/connect/userguide.html#connect-configuring-converters) (Confluent)
