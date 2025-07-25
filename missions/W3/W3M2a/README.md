# W3M2a - Docker의 Hadoop 단일 노드 클러스터

## 1. Docker 이미지 빌드

- Dockerfile자체는 M1과 큰 차이가 없음
1. jdk, ssh등 Hadoop 실행에 필요한 라이브러리 설치

## 2. 컨테이너 실행



## 3. HDFS 작업 수행

------------------

Hadoop 멀티 노드 클러스터 on Docker
이 프로젝트는 Docker와 Docker Compose를 사용하여 Apache Hadoop 3.3.6 멀티 노드 클러스터를 구축하는 방법을 안내합니다.

사전 요구사항
Docker

Docker Compose

프로젝트 구조
hadoop-multi-node-docker/
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── config/
│   ├── core-site.xml
│   ├── hadoop-env.sh
│   ├── hdfs-site.xml
│   ├── mapred-site.xml
│   ├── workers
│   └── yarn-site.xml
└── README.md

실행 방법
1. 클러스터 빌드 및 시작
프로젝트 루트 디렉토리에서 아래 명령어를 실행하여 Docker 이미지를 빌드하고 컨테이너를 시작합니다.

docker-compose up --build -d

2. 클러스터 상태 확인
클러스터가 정상적으로 실행되었는지 확인합니다.

컨테이너 확인: 1개의 namenode와 2개의 datanode가 실행 중이어야 합니다.

docker ps

웹 UI 접속:

HDFS NameNode UI: http://localhost:9870

YARN ResourceManager UI: http://localhost:8088

HDFS 웹 UI의 'Datanodes' 탭에서 2개의 활성 노드를 확인할 수 있습니다.

HDFS 및 MapReduce 작업 수행
1. NameNode 컨테이너 접속
HDFS 및 MapReduce 명령을 실행하기 위해 namenode 컨테이너의 셸에 접속합니다.

docker exec -it namenode /bin/bash

2. HDFS 파일 시스템 작업
namenode 컨테이너 내부에서 hadoop 사용자로 전환한 후 다음 명령을 실행합니다.

# hadoop 사용자로 변경
su - hadoop

# 디렉토리 생성
hdfs dfs -mkdir -p /user/hadoop/input

# 로컬 파일 생성 및 HDFS에 업로드
echo "hello hadoop hello world" > sample.txt
hdfs dfs -put sample.txt /user/hadoop/input

# 업로드된 파일 확인
hdfs dfs -ls /user/hadoop/input

3. MapReduce 작업 실행 (WordCount 예제)
hadoop 사용자 상태에서 Hadoop에 포함된 WordCount 예제를 실행합니다.

hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /user/hadoop/input /user/hadoop/output

4. MapReduce 결과 확인
작업이 완료되면 결과 파일의 내용을 확인합니다.

hdfs dfs -cat /user/hadoop/output/part-r-00000

결과로 hello 2, hadoop 1, world 1이 출력됩니다.

클러스터 종료
클러스터를 중지하고 관련 리소스(컨테이너, 네트워크)를 삭제하려면 다음 명령을 실행합니다.

docker-compose down

HDFS 데이터를 포함한 볼륨까지 완전히 삭제하려면 -v 옵션을 추가하세요: docker-compose down -v