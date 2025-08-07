FROM bitnami/spark:3.5

USER root

# 기본 유틸 설치
RUN apt-get update && apt-get install -y python3-pip curl git

# Jupyter 설치
RUN pip3 install --no-cache-dir notebook

# Jupyter 디렉토리 생성
RUN mkdir -p /opt/bitnami/work

WORKDIR /opt/bitnami/work

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''", "--notebook-dir=/opt/bitnami/"]