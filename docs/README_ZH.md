## Core平台介绍

Core是核心基础设施平台，提供能力与数据处理，向Triathon不断赋能。
Core平台的核心特点在于：我们融合了fuzzing-test的测试方法，以及混沌工程（实验）的概念，重新定义了区块链安全测试的方式。致力于建立了安全高效的web3测试环境。

## “CORE”平台特点

（将会在未来会不断更新）

1. （测试）工具建设：集合了各类测试工具，且未来将测试能力以API形式封装，提供给相关三方（如安全白帽）
2. API建设：CORE不断端漏洞转化成测试手段，并且变成API输出
3. 开发者管理：生态开发者基于API 生成全新NFT（测试服务）；或基于API应用后发现的漏洞提交
4. 漏洞转化 ：漏洞平台是 CORE 持续能力建设的一个核心组成

## 安装

### 环境安装

```
docker pull aug1/core-dev:1.0.2

docker run -it --name core -p 8000:8000 --privileged=true --restart always -v HostCodeDirectory:/opt/project aug1/core-dev:1.0.2

```

redis 6.2.6启动

postgres启动

#### 配置

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

#### api服务启动

```
docker exec -it core bash

nohup python backend/manage.py runserver 0:8000 >/opt/project/core-log/api 2>&1 &
```

#### 检测服务启动

##### python启动

```
nohup python coreslither/coreslither/handler.py >/opt/project/core-log/slither 2>&1 &
nohup python corethril/corethril/handler.py >/opt/project/core-log/thril 2>&1 &
nohup python coresmartian/coresmartian/handler.py >/opt/project/core-log/smartian 2>&1 &
```

##### faas-启动

```
...
```

## 使用

apifox  
链接: https://www.apifox.cn/apidoc/shared-979b9088-fd6a-4e65-8c96-c048c3edd188  访问密码 : x849iT7T 

1. 上传合约文件
   1. 本地文件上传
   2. 合约地址上传
2. 查看检测结果

---
Triathon官方邮箱：triathonspace@gmail.com
