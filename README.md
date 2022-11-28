# core

core平台集成了多种合同安全检测工具:slither, mythril...

**Core_slither**：Contract test items slither structure

**Corethril**：Contract test items mythril structure

## 安装使用

###环境安装启动
```
docker build -t core:v1 -f DockerfileDev .

docker run -it --name core -p 8000:8000 -v 宿主机代码目录:/opt/project core:v1

```
redis 6.2.6启动

postgres启动

####一. 配置
django服务配置
path: backend/conf/conf.json
```
{
  "db_host": "",
  "db_port": "",
  "db_name": "",
  "db_user": "",
  "db_password": "",
  "redis": "",
  "coreslither_queue": "coreslither",
  "corethril_queue": "corethril"
}
```
coreslither配置
path: coreslither/coreslither/config.conf
```
{
  "db_host": "",
  "db_port": "",
  "db_name": "",
  "db_user": "",
  "db_password": "",
  "redis_host": "",
  "redis_port": ,
  "redis_password":"",
  "redis_db":5,
  "task_queue": "coreslither"
}
```
corethril配置
path: corethril/corethril/config.conf
```
{
  "db_host": "",
  "db_port": "",
  "db_name": "",
  "db_user": "",
  "db_password": "",
  "redis_host": "",
  "redis_port": ,
  "redis_password":"",
  "redis_db":5,
  "task_queue": "corethril"
}
```
bsc/eth apikey配置
path: backend/api/tools/contract_helper.py
```
apikey = {"bsc": "",
          "eth": ""}
```



####二. api服务启动
```
docker exec -it core bash

nohup python backend/manage.py runserver 0:8000 >/opt/project/core-log/api 2>&1 &
```

#### 三. 检测服务启动

1.python启动
```
nohup python coreslither/coreslither/handler.py >/opt/project/core-log/slither 2>&1 &
nohup python corethril/corethril/handler.py >/opt/project/core-log/thril 2>&1 &

```

2.faas-启动
```
...
```

#### 三. api使用
apifox
链接: https://www.apifox.cn/apidoc/shared-979b9088-fd6a-4e65-8c96-c048c3edd188  访问密码 : x849iT7T 

1. 上传合约文件
    1. 本地文件上传
    2. 合约地址上传
2. 查看检测结果