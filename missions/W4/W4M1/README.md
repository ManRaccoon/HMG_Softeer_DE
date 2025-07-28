# W3M3 - Word Count using MapReduce

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

- **mapper.py, reducer.py, book.txt**를 이미지에 옮겨 MapReduce를 진행하도록 한다.

### ENTRYPOINT

- bash 실행 후 -lc 태그로 환경을 초기화하고 entrypoint.sh을 실행시키도록 한다.


## 2. 컨테이너 실행

- 이미지 빌드

```bash
docker compose up -d
```

## 3. MapReduce 작업 수행

Custom MapReduce 연산을 통해 입력한 e-book의 WordCount가 가능하도록 하였다.

- 선택한 E-book : Romeo and Juliet

https://www.gutenberg.org/ 사이트에서 저작권 만료 전자책을 가져옴

- namenode bash로 들어가기

```bash
docker exec -u hdfs -it namenode /bin/bash
```

- hdfs내에 /input 디렉토리 생성 및 E-book 파일 넣기

```bash
hdfs dfs -mkdir /input
```

```bash
hdfs dfs -put /book.txt /input/
```

- WordCount MapReduce 패키징 및 연산 진행

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
    -input /input/book.txt \
    -output /output/result \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -file mapper.py \
    -file reducer.py
```

- WordCount 연산 결과 확인

내림차순으로 상위 10개만 출력하도록 하였다.

```bash
hdfs dfs -cat /output/result/part-* | sort -k2,2nr | head -n 10
```

결과 출력

```bash
the: 780
I: 551
and: 541
to: 524
of: 476
a: 458
in: 350
is: 313
my: 304
with: 274
```

기능어 위주로 출력 결과가 나오는 것을 알 수 있었다. 불용어 사전에 기능어들을 맵핑해 놓는 전처리를 진행한 후 다시 진행하면 더 의미있는 결과가 나올 것이다.