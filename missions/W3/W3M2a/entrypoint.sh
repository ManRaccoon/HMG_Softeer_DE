# #!/bin/bash

# # 스크립트 실행 중 오류가 발생하면 즉시 중단합니다.
# set -e

# # 루트 권한으로 SSH 서비스를 먼저 시작합니다.
# # hadoop 사용자는 권한이 없으므로 반드시 루트로 실행해야 합니다.
# service ssh start

# # 컨테이너의 역할을 첫 번째 인자로부터 받습니다. (docker-compose.yml의 command에서 전달됨)
# ROLE=${HADOOP_ROLE}

# # 역할이 지정되지 않으면 오류를 출력하고 종료합니다.
# if [ -z "$ROLE" ]; then
#     echo "오류: 컨테이너 역할이 지정되지 않았습니다. ('namenode' 또는 'datanode')"
#     exit 1
# fi

# # 역할이 'namenode'일 경우
# if [[ "$ROLE" == "master" ]]; then
#     echo "NameNode로 설정 중입니다..."

#     # HDFS가 포맷되었는지 확인하고, 안 되어있으면 'hadoop' 사용자로 포맷을 실행합니다.
#     # NameNode 데이터 디렉토리가 있는지 확인합니다.
#     if [ ! -d "$HADOOP_HOME/data/namenode/current" ]; then
#         echo "NameNode를 포맷합니다..."
#         # 'su - hadoop -c'를 사용하여 hadoop 사용자로 명령을 실행합니다.
#         # su - hadoop -c "$HADOOP_HOME/bin/hdfs namenode -format -force"
#         "$HADOOP_HOME/bin/hdfs" namenode -format -force
#     else
#         echo "NameNode가 이미 포맷되어 있습니다."
#     fi

#     # 'hadoop' 사용자로 HDFS와 YARN 서비스를 시작합니다.
#     echo "HDFS와 YARN을 시작합니다..."
#     # su - hadoop -c "$HADOOP_HOME/sbin/start-dfs.sh"
#     # su - hadoop -c "$HADOOP_HOME/sbin/start-yarn.sh"
#     "$HADOOP_HOME/sbin/start-dfs.sh"
#     "$HADOOP_HOME/sbin/start-yarn.sh"
#     echo "NameNode 시작 완료."

# # 역할이 'datanode'일 경우
# elif [[ "$ROLE" == "worker" ]]; then
#     echo "DataNode로 설정 중입니다..."
#     # DataNode는 NameNode가 SSH를 통해 원격으로 데몬을 실행시킵니다.
#     # 따라서 이 컨테이너는 SSH 서비스만 켜두고 대기하면 됩니다.
#     echo "DataNode가 NameNode의 명령을 기다립니다."

# else
#     echo "오류: 잘못된 역할이 지정되었습니다: $ROLE"
#     exit 1
# fi

# # 컨테이너가 바로 종료되지 않도록 무한 대기 상태로 유지합니다.
# tail -f /dev/null

#!/bin/bash
set -e
service ssh start
ROLE=${HADOOP_ROLE}
if [[ "$ROLE" == "master" ]]; then
  # NameNode 포맷 & 기동
  gosu hadoop "$HADOOP_HOME/bin/hdfs" namenode -format -force
  gosu hadoop "$HADOOP_HOME/sbin/start-dfs.sh"
  gosu hadoop "$HADOOP_HOME/sbin/start-yarn.sh"
  tail -f /dev/null
else
  # 워커 노드
  service ssh start  # ensure sshd is running for pdsh
  tail -f /dev/null
fi