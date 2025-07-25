FROM ubuntu:20.04

ENV HADOOP_VERSION=3.3.6
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    openssh-server \
    openssh-client \
    openjdk-8-jdk \
    wget \
    gosu \
    pdsh && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt/ && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

ENV HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
ENV HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop
ENV HADOOP_MAPRED_HOME=${HADOOP_HOME}
ENV HADOOP_COMMON_HOME=${HADOOP_HOME}
ENV HADOOP_HDFS_HOME=${HADOOP_HOME}
ENV YARN_HOME=${HADOOP_HOME}
ENV PATH=$PATH:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin

RUN groupadd -r hadoop && useradd -r -g hadoop -m -d /home/hadoop -s /bin/bash hadoop

RUN mkdir -p /home/hadoop/.ssh \
    && chown hadoop:hadoop /home/hadoop/.ssh

RUN mkdir -p ${HADOOP_HOME}/logs \
    && chown -R hadoop:hadoop ${HADOOP_HOME}/logs

RUN mkdir -p ${HADOOP_HOME}/data/namenode ${HADOOP_HOME}/data/datanode && \
    chown -R hadoop:hadoop ${HADOOP_HOME}/data

RUN ssh-keygen -A && \
    ssh-keygen -t rsa -P '' -f /home/hadoop/.ssh/id_rsa && \
    cat /home/hadoop/.ssh/id_rsa.pub >> /home/hadoop/.ssh/authorized_keys && \
    chown -R hadoop:hadoop /home/hadoop/.ssh && \
    chmod 600 /home/hadoop/.ssh/authorized_keys

RUN echo "Host *" >> /home/hadoop/.ssh/config && \
    echo " StrictHostKeyChecking no" >> /home/hadoop/.ssh/config && \
    chown hadoop:hadoop /home/hadoop/.ssh/config && \
    chmod 600 /home/hadoop/.ssh/config

COPY config/* ${HADOOP_CONF_DIR}/

RUN mkdir -p /run/sshd \
    && chmod 0755 /run/sshd \
    && chown root:root /run/sshd


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN chown -R hadoop:hadoop ${HADOOP_HOME}

# USER hadoop

ENTRYPOINT ["/entrypoint.sh"]