# W3M2a - Hadoop Multi-Node Cluster on Docker

## 1. Docker 이미지 빌드

- Ubuntu 24.04 베이스이미지에 Hadoop 3.3.6을 실행시키는 이미지를 빌드하였습니다.
 
- Dockerfile 내 명령 실행을 기록해놓았습니다.

### FROM 명령어

- 베이스 이미지 명 : ubuntu:24.04

### ENV 명령어

- Hadoop 버전 = 3.3.6

- Hadoop 기본 디렉토리 위치

- JDK 기본 디렉토리 위치

- 환경변수 설정

파일을 실행하려면 그 디렉토리에 가야 하는 불편함이 있으므로, 명령어만으로 실행하기 위해 Hadoop폴더의 bin, sbin, JDK의 bin폴더를 환경변수로 설정해주었다.

### RUN 명령어

- apt 패키지 목록 최신화

- openjdk-11 다운로드

- wget, ssh, rsync, vim 다운로드

- hadoop 다운로드

### COPY 명령어

- config 디렉토리 안에 있는 모든 파일, entrypoint를 이미지에 옮긴다

### ENTRYPOINT

- bash 실행 후 -lc 태그로 환경을 초기화하고 entrypoint.sh을 실행시키도록 한다.


## 2. 컨테이너 실행

- 이미지 빌드

```bash
docker compose up -d
```

hadoop-single이라는 이름으로 도커 이미지 빌드


## 3. HDFS 작업 수행

Container 내부 명령어를 통해 MapReduce 연산이 가능하도록 하였다.

- namenode bash로 들어가기

```bash
docker exec -u hdfs -it namenode /bin/bash
```

- home 디렉토리로 이동

```bash
cd ~
```

- 예시 파일 작성

```bash
echo -e "Hello World\nWelcome to Hadoop\nHadoop MapReduce Example" > input.txt
```

- hdfs내에 /input 디렉토리 생성, 생성 확인

```bash
hdfs dfs -mkdir /input
```

```bash
hdfs dfs -ls /input
```

```bash
hdfs dfs -cat /input/input.txt
```

- wordcount MapReduce 연산 진행

```bash
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar wordcount /input /output
```

- MapReduce 연산 결과 확인

```bash
hdfs dfs -ls /output
```

```bash
hdfs dfs -cat /output/part-r-00000
```