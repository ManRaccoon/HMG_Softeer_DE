# W3M1 - Docker의 Hadoop 단일 노드 클러스터

## 1. Docker 이미지 빌드

- 

## 2. 컨테이너 실행

## 3. HDFS 작업 수행



docker build -t hadoop-single .

docker run -d --name hadoop \  
  -p 9870:9870 -p 8088:8088 \
  -v hdfs_namenode:/usr/local/hadoop-3.3.6/hdfs/namenode \
  -v hdfs_datanode:/usr/local/hadoop-3.3.6/hdfs/datanode \
  hadoop-single


  당시 문제
증상·오류 메시지
근본 원인
잘못된 JAVA_HOME
ERROR: JAVA_HOME is not set
ENV JAVA_HOME과 실제 JDK 설치 경로(arm64 vs amd64) 불일치.

설정 파일 위치 오류
NameNode가 기본 설정으로 기동 → 사용자 설정 미반영
XML을 $HADOOP_HOME/ 루트로 복사. Hadoop은 etc/hadoop/만 읽음.

pdsh rsh 의존
pdsh@<컨테이너>: connect: Connection refused
pdsh가 rsh(514) 프로토콜을 기본 사용, rshd 미설치.

pdsh ssh 플러그인 누락
pdsh: unknown rcmd type “ssh” (또는 255 종료)
pdsh-mod-ssh / pdsh-rcmd-ssh 패키지를 찾지 못하거나 이름 오류.

host key·/var/run/sshd 없음
service ssh start 직후 sshd 즉시 종료 → 포트 22 비어 → 연결 거절
host key 미생성(Could not load host key …) 또는 런타임 디렉터리 미존재.

authorized_keys 권한 오류
Authentication refused: bad ownership …authorized_keys
/root/.ssh 700, authorized_keys 600이 아니어서 sshd가 인증 차단.

rsh 오류 해결 후에도 포트만 IPv6 LISTEN
pdsh가 ssh지만 여전히 connection refused
sshd가 :::22(IPv6)만 듣고 0.0.0.0:22 안 열림 → ListenAddress 0.0.0.0 필요.

빌드 단계 apt 404
E: Unable to locate package … → exit code 100
arm64 저장소에 없는 패키지( pdsh-rcmd-ssh, openjdk-8-jdk-headless 등) 지정.

PATH 누락
/entrypoint.sh: hdfs: command not found
login-shell이 아니어서 $HADOOP_HOME/bin이 PATH에 없음.

포맷을 매 컨테이너 시작 때마다 실행
HDFS 데이터 매번 초기화


docker run -d --name hadoop \
  -p 9870:9870 -p 8088:8088 -p 9864:9864 \
  -v hdfs_namenode:/usr/local/hadoop-3.3.6/hdfs/namenode \
  -v hdfs_datanode:/usr/local/hadoop-3.3.6/hdfs/datanode \
  hadoop-single