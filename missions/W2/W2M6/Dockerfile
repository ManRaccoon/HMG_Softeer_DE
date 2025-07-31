# FROM : 베이스 이미지 선택
FROM ubuntu:20.04

# EXPOSE : 포트번호 설정
EXPOSE 8888

# 작업 환경 디렉토리 설정
WORKDIR /home

# 이미지 생성 시 수행되는 명령어들
RUN \
    apt update && \
    apt install python3-pip && \
    pip install jupyter && \
    apt install git && \
    git clone https://github.com/ManRaccoon/HMG_Softeer_DE.git

WORKDIR /home/HMG_Softeer_DE/missions/W1

# ENTRYPOINT : 컨테이너 실행 시마다 동작하는 명령어
ENTRYPOINT ["jupyter", "notebook", "--allow-root"]

# CMD
CMD ["--ip=0.0.0.0", "--port=8888", "--NotebookApp.token=''"]

# jupyter notebook --allow-root --ip=0.0.0.0 --port=8890 