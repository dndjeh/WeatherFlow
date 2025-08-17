FROM openjdk:17-jdk-slim

WORKDIR /app

COPY producer.py .
COPY consumer.py .
COPY preprocessing.py .
COPY .env .
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-distutils curl && \
    apt-get clean

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir pyspark==3.5.5 pymysql sqlalchemy

ENV SPARK_PACKAGES="org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,mysql:mysql-connector-java:8.0.33"
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH
