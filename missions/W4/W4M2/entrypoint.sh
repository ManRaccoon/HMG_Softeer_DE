#!/usr/bin/env bash
set -e
mkdir -p $HADOOP_HOME/logs $SPARK_HOME/logs
# touch $HADOOP_HOME/logs/dummy.log
# touch $SPARK_HOME/logs/dummy.log

if [ "$HOSTNAME" == "namenode" ]; then
    if [ ! -f /usr/local/hadoop/tmp/dfs/name/current/VERSION ]; then
        $HADOOP_HOME/bin/hdfs namenode -format -force
    fi
    $HADOOP_HOME/bin/hdfs namenode &
elif [[ "$HOSTNAME" == datanode* ]]; then
    $HADOOP_HOME/bin/hdfs datanode &
elif [ "$HOSTNAME" == "master" ]; then
    $SPARK_HOME/sbin/start-master.sh &
elif [[ "$HOSTNAME" == slave* ]]; then
    $SPARK_HOME/sbin/start-worker.sh spark://master:7077 &
fi

tail -F $HADOOP_HOME/logs/* $SPARK_HOME/logs/*