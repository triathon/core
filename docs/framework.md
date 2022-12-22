### 技术架构

![](.\image.png)

##### 项目核心检测服务采用OpenFaas架构开发，基于Serverless架构，kubernetes为基础的函数式容器服务.在OpenFaaS内部为一个个运行着的合约检测服务，每个检测服务都有着对应着的API，将路径指定为URL的一部分，每个功能都为Kubernetes的服务，具有多个副本。就像任何其他Kubernetes工作负载一样，它可以扩展和所见并处理多个并发请求并方便未来升级的去中心化云原生服务中。
