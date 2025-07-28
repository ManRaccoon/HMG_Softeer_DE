FROM ubuntu:24.04

ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/usr/local/hadoop
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$JAVA_HOME/bin

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

RUN groupadd hadoop && \
    useradd -ms /bin/bash -g hadoop hdfs && \
    useradd -ms /bin/bash -g hadoop yarn

RUN chown -R hdfs:hadoop $HADOOP_HOME && \
    chmod -R 775 $HADOOP_HOME

COPY config/*.xml /usr/local/hadoop/etc/hadoop/

# input ebook, mapper, reducer for wordcount
COPY mapper.py /mapper.py
RUN chmod +x /mapper.py
COPY reducer.py /reducer.py
RUN chmod +x /reducer.py
COPY book.txt /book.txt
RUN chmod +x /book.txt

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]