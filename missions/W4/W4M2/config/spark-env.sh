#!/usr/bin/env bash
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop
export SPARK_MASTER_HOST=master
export SPARK_WORKER_CORES=2
export SPARK_WORKER_MEMORY=2g
export SPARK_DIST_CLASSPATH=$(hadoop classpath)