# 1. core-site.xml
모든 Hadoop 컴포넌트에서 공통으로 참조하는 기본 설정을 담당하는 파일이다.

- fs.defaultFS : file system URI를 명시하는 파라미터. Hadoop은 여러 종류의 파일 시스템을 지원하기에, 어디서 데이터를 읽고 쓸 것인지 명확히 지정하기 위해 URI 형식이 사용된다. 클러스터 구조가 변경될 시(예: NameNode 주소 변경, 다른 파일 시스템으로 마이그레이션 등) 이 값을 수정하면 클러스터 전체 경로 해석 방식이 바뀐다.
  - [scheme]://[authority]:port
  - hdfs://host:port/

- hadoop.tmp.dir : Hadoop component가 사용하는 기본 임시 디렉터리. NameNode, DataNode, ResourceManager 등 여러 컴포넌트가 공통적으로 사용하는 기본 임시 저장소이다. 만약 dfs.namenode.name.dir이 설정되면 무시된다.
  
- io.file.buffer.size : SequenceFile에서 사용되는, Read/Write Buffer 사이즈를 조정하기 위한 파라미터. 데이터셋의 특성에 따라 입출력 속도가 다른데, 그에 따라 해당 파라미터를 바꿔 속도를 조절한다. 예를 들어 작은 사이즈의 파일을 자주 다루는 경우 너무 큰 버퍼는 낭비이며, 반면 대용량 파일을 순차 처리하는 경우 버퍼를 키워 성능 향상이 가능하다.
  - default : 131072 Bytes = 128 KB


# 2. hdfs-site.xml
HDFS의 핵심 설정을 담당하는 설정파일로, HDFS 저장소의 구조, 복제, 블록 크기, 네임노드/데이터노드 관련 설정을 담당한다.

## (1) namenode 관련 설정
- dfs.namenode.name.dir : NameNode 메타데이터(파일 시스템 이미지와 로그 등)를 저장할 로컬 디렉토리 경로를 설정하는 파라미터. NameNode의 경로가 바뀌는 경우는 기존 저장 디스크의 용량이 부족하여 교체하는 등 다른 디스크에 저장하고 싶을 때 발생한다.
  
- dfs.hosts / dfs.hosts.exclude: HDFS에서 DataNode 접근 제어를 위해 사용되는 설정. NameNode가 어떤 노드를 허용할지 또는 제외할지 지정. 즉, 여기에 명시된 호스트만 Datanode로 참여시키거나, 제외시킴.

- dfs.blocksize: 블록 사이즈를 정의하는 파라미터. block이란, 파일을 일정 크기의 덩어리로 나눈 것. HDFS는 일반 파일 시스템처럼 파일을 통째로 저장하지 않고, 대신 파일을 고정 크기 블록들로 쪼개고, 각 블록을 DataNode에 분산 저장한다.
  - default = 268435456 (256MB for large file-systems)
  
- dfs.namenode.handler.count : HDFS의 NameNode가 동시에 처리할 수 있는 클라이언트 요청의 수를 설정하는 파라미터. NameNode는 HDFS 명령어 또는 DataNode에서 오는 요청 등을 처리하기 위해 여러 개의 스레드를 띄워두는데, 이 스레드들은 파일 읽기, 메타데이터 조회, 파일 목록 조회 등 HDFS 메타데이터 관련 요청을 처리한다. 이렇게 최대 띄울 수 있는 스레드의 개수를 설정해둔다. 단, 스레드가 너무 적으면 성능이 떨어지고, 스레드가 너무 많으면 컨텍스트 스위칭 비용이 늘어난다.
  - default : 100
  
- dfs.replication: replica의 수를 설정한다. replica의 수를 늘리면 유지보수성이 늘어난다. 예를 들어 특정 노드가 과부하되거나 유지보수로 내려가도, 다른 노드의 복제본을 활용할 수 있는 가능성이 높아진다.
    - default = 3 (하나의 HDFS 블록이 서로 다른 3개의 DataNode에 복제되어 저장)
  
## (2) datanode 관련 설정
- dfs.datanode.data.dir : 파일 시스템이 꽉 차서 디스크 추가/마운트될 때 일반적으로 DataNode의 데이터 저장 경로 수정.


# 3. map-red.xml
MapReduce는 Map, Shuffle, Reduce의 3단계로 이루어져있으며, 각각에 대한 설정 파일이다.

## (1) MapReduce 관련 설정
- mapreduce.framework.name: 실행하는 프레임워크를 yarn으로 설정한다.
  
- mapreduce.map.memory.mb : 각 Map task가 실행될 컨테이너의 전체 메모리 크기(MB). 컨테이너에 할당할 총 메모리 (heap + non-heap 포함)를 의미.
  - default : 1536
  
- mapreduce.reduce.memory.mb : 각 Reduce task가 실행될 컨테이너 메모리 크기(MB). Reduce는 Map보다 복잡하므로 더 많은 메모리가 필요하다.
  - default: 3072

- mapreduce.task.io.sort.mb: MapReduce에서 map 작업 결과를 정렬하고 버퍼링하기 위해 사용하는 메모리 버퍼 크기를 지정하는 파라미터. 입력 split → map() 함수 → (key, value) 출력 → 메모리에 임시 저장 → 정렬 → 디스크 spill → shuffle 순서로 진행되는데, 여기서 디스크로 spill(쓰기)하기 전에, 임시저장 및 정렬에 사용하는 메모리 양을 지정.

- mapreduce.task.io.sort.factor : Spill 파일을 병합할 때 동시에 열 수 있는 파일 수. 값이 너무 작으면 병합이 여러 번 발생하여 성능이 저하된다.
  - default : 10

- mapreduce.reduce.shuffle.parallelcopies : 각 Reduce task가 동시에 Map task로부터 데이터를 받아올 수 있는 연결 수. 너무 작으면 shuffle 병목이 발생해서 매우 느려지고, 너무 크면 네트워크 부하가 걸릴 수 있다.
  - default: 5

## (2) MapReduce JobHistory Server 관련 설정
- mapreduce.jobhistory.address: Mapreduce 작업의 실행 이력을 조회할 수 있는 history server의 주소를 지정하는 파라미터. MapReduce 작업의 상태, 로그, 성능 지표를 조회할 때 연결한다.
  
- mapreduce.jobhistory.webapp.address: JobHistory 서버의 웹 UI 주소 (호스트:포트) 를 지정.
  - namenode:19888

- mapreduce.jobhistory.intermediate-done-dir: 진행 중이거나 방금 끝난 Job의 이력 파일(jhist 등)을 저장하는 임시 디렉토리. 이 디렉토리는 History 서버가 주기적으로 스캔하여 .jhist 파일을 done-dir로 이동시킨다.
  - hdfs:///mr-history/tmp
  
- mapreduce.jobhistory.done-dir: 완료된 MapReduce Job들의 로그 파일들을 영구 저장하는 디렉토리. JobHistory 서버는 이 디렉토리를 기준으로 웹 UI에서 작업 이력을 제공한다.
  - hdfs:///mr-history/done

# 4. yarn-site.xml
## (1) ResourceManager, NodeManager 공통 설정
- yarn.acl.enable: YARN 리소스에 대한 접근 제어(사용자/그룹 기반 권한 설정)를 활성화할지 여부를 지정.
  - default: false
  
- yarn.scheduler.minimum-allocation-mb: yarn에서 어떤 작업이 들어오면, AM에게 전달되어 NodeManager에게 컨테이너(자원)을 요청한다. 자원이 도착하면 각 컨테이너를 ResourceManager에게 전달하고, ResourceManager는 이 자원을 가지고 요청된 작업을 실행하도록 전달한다. 이때 각 컨테이너에 할당되어야 하는 최소 메모리를 지정하는 파라미터이다. 

## (2) ResourceManager 관련 설정
- yarn.resourcemanager.address: Yarn 클러스터에서 클라이언트가 ResourceManager에 접근할 때 사용하는 주소. (RPC: 여러 노드로 구성된 분산시스템에서 네트워크를 통해 다른 서버에 있는 메서드를 호출. 마치 로컬 함수처럼 사용하지만 내부적으로 네트워크 통신이 발생.)

- yarn.nodemanager.resource.memory-mb: Yarn에서 해당 노드가 컨테이너 실행을 위해 사용할 수 있는 총 메모리의 용량을 설정하는 파라미터. 한 노드가 최대 얼마만큼의 메모리를 컨테이너들에게 나눠줄 수 있는지를 알려주는 설정.

## (3) NodeManager 관련 설정
- yarn.nodemanager.resource.memory-mb: NodeManager가 사용할 수 있는 전체 메모리 용량을 MB 단위로 지정. YARN에서 실행되는 각 컨테이너는 이 메모리 범위 내에서 동작해야 함.
  - 반드시 mapreduce.map.memory.mb, mapreduce.reduce.memory.mb와 일관되게 설정되어야 함.
  
- yarn.nodemanager.aux-services: NodeManager가 제공해야 할 보조(Auxiliary) 서비스들을 명시하는 설정.
  - mapreduce_shuffle: MapReduce를 실행하기 위해 반드시 설정해야함.


---

# W3M4 'predefined keywords' 외 다른 분류 방법

'미리 정의된 키워드' 방식은 간단하지만, 문맥이나 새로운 신조어를 이해하지 못하는 명확한 한계가 있습니다. 이를 극복하기 위한 더 정교한 방법들이 있으며, 크게 **전통적인 머신러닝**과 **딥러닝** 두 가지 방향으로 나눌 수 있습니다.

---

##  1. 전통적인 머신러닝 (Traditional Machine Learning)

이 접근 방식은 텍스트의 통계적 특징을 추출하여 **특징 벡터(Feature Vector)** 로 변환한 뒤, 이 벡터를 분류 모델에 학습시키는 방법입니다.

### **어떻게 다른가요?**

키워드 방식이 단순히 'good'이라는 단어의 유무를 본다면, 머신러닝은 'good'이라는 단어가 얼마나 자주 등장하는지(TF), 다른 문서에서는 얼마나 드물게 나타나는지(IDF) 등의 통계적 중요도를 계산하여 문맥을 파악합니다.

### **적용 방법**

1.  **특징 추출 (Feature Extraction): TF-IDF**
    * 가장 널리 쓰이는 방법은 **TF-IDF(Term Frequency-Inverse Document Frequency)** 입니다.
    * **TF(단어 빈도)**: 한 트윗 안에서 특정 단어가 얼마나 자주 등장하는지를 나타냅니다.
    * **IDF(역문서 빈도)**: 전체 트윗 데이터에서 특정 단어가 얼마나 희귀한지를 나타냅니다. 'the', 'a'처럼 자주 나오는 단어는 낮은 가중치를, 'awesome', 'terrible'처럼 특정 감성과 연관된 단어는 높은 가중치를 받게 됩니다.
    * 결과적으로 각 트윗은 수많은 숫자로 이루어진 **TF-IDF 벡터**로 표현됩니다.

2.  **모델 학습 및 예측 (Model Training & Prediction)**
    * **학습**: 레이블이 있는 데이터(Sentiment140의 긍정/부정 레이블)를 사용하여 TF-IDF 벡터와 감성 레이블 간의 관계를 **나이브 베이즈(Naive Bayes)**, **로지스틱 회귀(Logistic Regression)** 등의 모델에 학습시킵니다.
    * **맵리듀스 적용**:
        * **Mapper**: 미리 학습된 모델과 TF-IDF 변환기를 불러옵니다. 각 트윗 텍스트를 TF-IDF 벡터로 변환한 뒤, 모델에 입력하여 'positive', 'negative' 등을 예측합니다. 예측된 결과를 Key로 하여 `('positive', 1)`과 같이 출력합니다.
        * **Reducer**: 기존과 동일하게 Key별로 개수를 집계합니다.

---

##  2. 딥러닝 - 사전 훈련된 모델 활용 (Deep Learning - Using Pre-trained Models)

최근 가장 성능이 뛰어난 방법으로, 대규모 텍스트 데이터로 미리 학습된 언어 모델을 사용하여 문장의 **문맥적 의미** 자체를 이해하고 감성을 분석합니다.

### **어떻게 다른가요?**

"This is not good at all."이라는 문장에서, 키워드 방식은 'good' 때문에 긍정으로 오해할 수 있지만, 딥러닝 모델은 'not'과 'at all'의 관계를 통해 전체 문장이 부정이라는 것을 **문맥적으로 파악**합니다.

### **적용 방법**

1.  **사전 훈련된 언어 모델 (Pre-trained Language Models): BERT, RoBERTa 등**
    * **BERT(Bidirectional Encoder Representations from Transformers)** 와 같은 모델들은 수많은 책, 위키피디아 등의 텍스트로 언어의 복잡한 패턴을 미리 학습했습니다.
    * 이 모델들을 감성 분석용 데이터로 **미세 조정(Fine-tuning)** 하여 특정 작업에 최적화시킬 수 있습니다.

2.  **맵리듀스/스파크 적용**:
    * 딥러닝 모델은 크고 복잡하여 일반적인 하둡 스트리밍보다는 **스파크(Spark)** 와 함께 사용하는 것이 더 효율적입니다.
    * **Mapper (또는 Spark UDF)**: 미세 조정된 딥러닝 모델(예: Hugging Face 라이브러리 모델)을 불러옵니다. 각 트윗 텍스트를 모델에 직접 입력하면, 모델이 알아서 토큰화, 임베딩, 문맥 분석을 수행하여 최종 감성('positive', 'negative', 'neutral')을 반환합니다. 이 결과를 Key로 출력합니다.
    * **Reducer**: 동일하게 개수를 집계합니다.

---

##  방법별 비교 요약

| 방법 (Method)                               | 장점 (Pros)                                                                     | 단점 (Cons)                                                                  |
| ------------------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **1. 키워드 기반** (Keyword-based)          | 구현이 매우 간단하고 빠름.                                                      | 문맥, 신조어, 비꼬는 표현 등을 전혀 이해하지 못함. 정확도가 낮음.             |
| **2. 전통적 머신러닝** (Traditional ML)     | 키워드보다 훨씬 높은 정확도. 데이터의 통계적 패턴을 학습함.                       | 특징 추출 과정이 필요하며, 복잡한 문장 구조의 의미 파악에는 한계가 있음.       |
| **3. 딥러닝 모델** (Deep Learning Models) | **가장 높은 정확도**. 문맥, 뉘앙스, 비꼬는 표현까지 이해 가능. | 모델이 매우 크고 무거워 높은 컴퓨팅 자원(GPU 등)이 필요함. 예측 속도가 느림. |