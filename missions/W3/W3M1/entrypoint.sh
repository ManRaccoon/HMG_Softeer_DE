#!/bin/bash
set -ex
# pdsh가 기본 rsh 대신 ssh를 사용하도록 강제
export PDSH_RCMD_TYPE=ssh

service ssh start

# NameNode 메타데이터가 없을 때만 최초 1회 포맷
if [ ! -f "$HADOOP_HOME/hdfs/namenode/current/VERSION" ]; then
    "$HADOOP_HOME/bin/hdfs" namenode -format -force -nonInteractive
fi

start-dfs.sh
start-yarn.sh

echo "Hadoop is up!  NameNode UI → http://localhost:9870"

# 컨테이너가 종료되지 않도록 대기
tail -f /dev/null