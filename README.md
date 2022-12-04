# core

Core平台的核心服务，基于Serverless架构，以Kubernetes为基础生成的函数式容器服务。

基于OpenFaaS的无服务计算WatchDog，进行模块可插拔和弹性伸缩；在OpenFaaS内部为一个个运行着的合约检测服务，每个检测服务都有着对应着的API，将路径指定为
URL的一部分，每个功能都为Kubernetes的服务，具有多个副本。就像任何其他Kubernetes工作负载
一样，它可以扩展和所见并处理多个并发请求并方便未来升级的去中心化云原生服务中。


**Core_slither**：Contract test items slither structure

**Corethril**：Contract test items mythril structure

**CoreSmartian**：Contract test items Smartian fuzzy

## 安装使用

###环境安装启动
```
docker build -t core:v1 -f DockerfileDev .

docker run -it --name core -p 8000:8000 -v 宿主机代码目录:/opt/project core:v1

```
redis 6.2.6启动

postgres启动

#### 一. 配置
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
coreSmartian配置
path: coresmartian/coresmartian/config.conf

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
  "task_queue": "coresmartian"
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
nohup python coresmartian/coresmartian/handler.py >/opt/project/core-log/smartian 2>&1 &

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