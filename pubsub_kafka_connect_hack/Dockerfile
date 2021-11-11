FROM debian:10

WORKDIR /pubsub_kafka

COPY . .

RUN apt-get update &&\
   apt-get install -y wget less nano gnupg software-properties-common

RUN apt-get update &&\
   apt-get install -y default-jre

RUN apt-get update &&\
   apt-get install -y default-jdk

RUN echo 'JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64/bin/java"' >> /etc/environment

RUN wget -qO - https://packages.confluent.io/deb/6.0/archive.key | apt-key add -

RUN add-apt-repository "deb [arch=amd64] https://packages.confluent.io/deb/6.0 stable main"

RUN apt-get update && apt-get install -y confluent-platform

WORKDIR /usr/local/share/kafka/plugins

RUN wget https://github.com/GoogleCloudPlatform/pubsub/releases/download/v0.10-alpha/pubsub-kafka-connector.jar

WORKDIR /pubsub_kafka
