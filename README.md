## What is CORE platform?
As a vital infrastructure platform, CORE empowers Triathon by providing data processing service and other capabilitties continuously.
In the CORE platform, we incorporate the fuzzing-test testing method and the concept of chaos engineering (experimental) to redefine the way of blockchain security testing. We're committed to establishing a safe and efficient web3 testing environment.

## Main utilities of “CORE”
 (The platform will be constantly updated in the future.)
1. (Testing) Tool building: a collection of various testing tools. Testing capabilities will be packaged in the form of API and be provided to third parties including security white hats in the future.
2. API building: CORE continuously converts vulnerabilities into testing methods and outputs APIs.
3. Developer management: Eco-developers mint new NFT (i. e. test service) based on API; or they can report vulnerabilities based on their use of the API application.
4. Vulnerability conversion: The vulnerability platform is a key component of CORE’s continuous capacity building.

## Installation 
### Install the environment

```
docker build -t core:v1 -f DockerfileDev .

docker run -it --name core -p 8000:8000 -v 宿主机代码目录:/opt/project core:v1

```

redis 6.2.6 install
postgres install

#### configuration

django service configuration

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

coreslither configuration

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

corethril configuration

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

coreSmartian configuration
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

bsc/eth API Keys configuration

path: backend/api/tools/contract_helper.py

```
apikey = {"bsc": "",
          "eth": ""}
```


#### API service run

```
docker exec -it core bash

nohup python backend/manage.py runserver 0:8000 >/opt/project/core-log/api 2>&1 &
```

#### Detection service run

##### Python run

```
nohup python coreslither/coreslither/handler.py >/opt/project/core-log/slither 2>&1 &
nohup python corethril/corethril/handler.py >/opt/project/core-log/thril 2>&1 &
nohup python coresmartian/coresmartian/handler.py >/opt/project/core-log/smartian 2>&1 &
```

##### FaaS- run

```
...
```

## How to use the API?
apifox link: 
https://www.apifox.cn/apidoc/shared-979b9088-fd6a-4e65-8c96-c048c3edd188 password: x849iT7T
1. Upload the smart contract file
     i. Local file upload
     ii. Contract address upload

2. View test results

---
Triathon official mailbox：triathonspace@gmail.com