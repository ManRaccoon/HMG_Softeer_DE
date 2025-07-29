FROM ubuntu:24.04

ENV HADOOP_VERSION=3.3.6
ENV SPARK_VERSION=3.4.1
ENV HADOOP_HOME=/usr/local/hadoop
ENV SPARK_HOME=/usr/local/spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin

RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget \
    ssh \
    rsync \
    vim \
    && apt-get clean

RUN wget https://mirrors.sonic.net/apache/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar xvzf hadoop-$HADOOP_VERSION.tar.gz && \
    mv hadoop-$HADOOP_VERSION $HADOOP_HOME && \
    rm hadoop-$HADOOP_VERSION.tar.gz

RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-without-hadoop.tgz && \
    tar xvzf spark-${SPARK_VERSION}-bin-without-hadoop.tgz && \
    mv spark-${SPARK_VERSION}-bin-without-hadoop $SPARK_HOME && \
    rm spark-${SPARK_VERSION}-bin-without-hadoop.tgz


RUN groupadd hadoop && \
    groupadd spark && \
    useradd -ms /bin/bash -g spark hdfs && \
    useradd -ms /bin/bash -g spark spark

RUN chown -R hdfs:spark $HADOOP_HOME && \
    chmod -R 775 $HADOOP_HOME && \
    chown -R spark:spark $SPARK_HOME && \
    chmod -R 775 $SPARK_HOME

COPY config/spark-env.sh /usr/local/spark/conf/spark-env.sh
COPY config/slaves /usr/local/spark/conf/slaves

COPY config/*.xml /usr/local/hadoop/etc/hadoop/

COPY pi.py /pi.py
RUN chmod +x /pi.py

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]