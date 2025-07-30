# W3M3 - Word Count using MapReduce

## Spark pi.py 작업 실행

- docker bash로 들어가기

```bash
docker exec -u hdfs -it namenode /bin/bash
```

- hdfs내에 /output 디렉토리 생성

```bash
hdfs dfs -mkdir /output
```

- pi.py실행 및 결과 저장

```bash
spark-submit \
--master spark://master:7077 \
--deploy-mode client \
/pi.py \
1000 \
hdfs://namenode:9000/output/pi
```

- WordCount 연산 결과 확인

내림차순으로 상위 10개만 출력하도록 하였다.

```bash
hdfs dfs -cat /output/pi/part-*
```

결과 출력 예시

```bash
3.14532
```