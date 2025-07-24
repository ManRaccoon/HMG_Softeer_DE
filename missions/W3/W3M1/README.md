# W3M1 - Docker의 Hadoop 단일 노드 클러스터

## 1. Docker 이미지 빌드

- Ubuntu 20.04 베이스이미지에 Hadoop 3.3.6을 실행시키는 이미지를 빌드하였습니다.
 
- Dockerfile 내 명령 실행을 기록해놓았습니다.

### FROM 명령어

- 베이스 이미지 명 : ubuntu:20.24

### ENV 명령어

- Hadoop 버전

- Hadoop 기본 디렉토리 위치

- JDK 기본 디렉토리 위치

- 환경변수 설정

파일을 실행하려면 그 디렉토리에 가야 하는 불편함이 있으므로, 명령어만으로 실행하기 위해 Hadoop폴더의 bin, sbin, JDK의 bin폴더를 환경변수로 설정해주었다.

- 하둡 데몬 계정 설정

격리되어있는 컨테이너 내에서 자유롭게 하둡을 이용할 수 있도록 root권한을 주었다.

### RUN 명령어

- apt 패키지 목록 최신화

- openjdk-8 다운로드

- ssh server, ssh client 다운로드

일반 ssh만 다운할 경우 원하는 패키지가 포함되지 않을 가능성이 있으므로 정확히 명시하여 ssh통신을 할 수 있도록 하였다.

- net-tools, iproute2 다운로드

컨테이너 내에서 통신이 진행되지 않는 문제가 있었으므로, 네트워크 디버깅을 위한 툴을 설치하여 다시 도커이미지 빌드하기 전에 container 내에서 문제를 확인하고자 하였다.

- sshd 작업 디렉토리 생성 및 서버 식별을 위한 호스트 키 생성
    
이 디렉토리가 존재하지 않을 경우 sshd통신 시작이 실패하는 경우가 있어 가져옴

서버 식별용 키 세트가 없으면 sshd가 클라이언트 연결을 거부할 수 있음

- 루트 사용자가 암호 없이 로그인하도록 키 생성

- Hadoop 3.3.6 다운로드 및 ENV에서 설정한 경로로 압축 해제 및 이동

### COPY 명령어

#### 로컬에 있는 Hadoop 설정파일 복사

- core-site.xml : 하둡 공통 설정

- hdfs-site.xml : HDFS 전용 설정

- mapred-site.xml : MapReduce 설정 (이번 미션에서는 사용하지 않음)

- yarn-site.xml : YARN 설정 (이번 미션에서는 사용하지 않음)

- 컨테이너 시작 시 실행할 쉘 스크립트 entrypoint.sh 복사 및 실행권한 설정

### EXPOSE 명령어

#### 이미지 내에 포트 사용 정보 명시함

- 9870 : NameNode Web UI

- 9864 : DataNode Web UI

- 8088 : YARN Web UI (이번 미션에서는 사용하지 않음)

- 9000 : NameNode RPC 포트 (이번 미션에서는 사용하지 않음)

### ENTRYPOINT

#### 컨테이너 실행 시 지정명령을 반드시 수행하게 함

bash 실행 후 -lc 태그로 환경을 초기화하고 entrypoint.sh을 실행시키도록 한다.


## 2. 컨테이너 실행

- 이미지 빌드

```bash
docker build -t hadoop-single .
```

hadoop-single이라는 이름으로 도커 이미지 빌드

- 이미지를 통한 컨테이너 실행

```bash
docker run -d --name hadoop \
-p 9870:9870 -p 8088:8088 -p 9864:9864 \
-v hdfs_namenode:/usr/local/hadoop-3.3.6/hdfs/namenode \
-v hdfs_datanode:/usr/local/hadoop-3.3.6/hdfs/datanode \
hadoop-single
```

빌드된 이미지(hadoop-single)로 hadoop이라는 Container로 백그라운드 실행

9870, 8088, 9864 포트 매핑 설정 (호스트:컨테이너 내 포트) -> localhost:9870으로 접근 위해

hdfs_namenode, hdfs_datanode를 로컬 블록 저장 디렉토리에 연결하여 컨테이너 재실행 시에도 포맷 없이 재사용 가능

- 실행 이후 docker desktop에 들어가면 실행되는 것을 알 수 있다.

## 3. HDFS 작업 수행

Container 내부 명령어를 통해 디렉토리 생성, 파일 업로드, 파일 검색이 가능하도록 하였다.

- 디렉토리 생성

localhost:9870를 컨테이너 밖에서 실행 후 디렉토리 생성이 가능하다는 것을 확인하였다.

```bash
hdfs dfs -mkdir /hadoop-user
```

- 로컬 파일 업로드

컨테이너 내에 'hi.txt'라는 파일을 업로드하도록 하였다. localhost:9870의 웹 UI에서는 업로드를 통해 컨테이너 밖의 요소도 업로드가 가능하다는 것을 확인하였다.

```bash
hdfs dfs -put /hi.txt /hadoop-user/
```

- 업로드 된 파일 검색

해당 파일이 들어있는 디렉토리 내의 요소에 대해 와일드카드 문자를 포함한 문자열 검색을 수행할 수 있음. localhost:9870 내에서도 마찬가지인 것을 확인하였다.

```bash
hdfs dfs -find /hadoop-user -name "*.txt"
```