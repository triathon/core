FROM python:3.8.9-slim
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install gcc libpq-dev -y &&\
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
