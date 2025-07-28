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
elif [ "$HOSTNAME" == "resourcemanager" ]; then
    $HADOOP_HOME/bin/yarn resourcemanager
elif [[ "$HOSTNAME" == nodemanager* ]]; then
    $HADOOP_HOME/bin/yarn nodemanager
fi

tail -f /dev/null