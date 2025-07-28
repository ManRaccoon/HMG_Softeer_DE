#!/bin/bash
if [ "$HOSTNAME" == "namenode" ]; then
    if [ ! -f /usr/local/hadoop/tmp/dfs/name/current/VERSION ]; then
        $HADOOP_HOME/bin/hdfs namenode -format -force
    fi
fi

if [ "$HOSTNAME" == "namenode" ]; then
    $HADOOP_HOME/bin/hdfs namenode
elif [[ "$HOSTNAME" == datanode* ]]; then
    $HADOOP_HOME/bin/hdfs datanode
elif [ "$HOSTNAME" == "driver" ]; then
    $SPARK_HOME/sbin/start-master.sh
elif [[ "$HOSTNAME" == worker* ]]; then
    $SPARK_HOME/sbin/start-slave.sh spark://driver:7077
fi

tail -f /dev/null