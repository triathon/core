# Core2c

# 代码说明

以下全部说明是以在当前文件夹下为前提

## 1 代码
git地址: https://github.com/triathon/core

main: 主分支

代码文件夹: core2c
## 2 环境构建

需在当前目录下构建镜像
### 2.1 开发环境构建

文件夹下的dev.dockerfile是开发环境的docker镜像构建文件，使用该文件构建镜像后可以使用开发工具在容器内进行开发。

### 2.2 生产环境构建

文件夹下的dockerfile是生产环境的docker镜像构建文件

## 3 数据库
PostgreSQL 12.0 \
在db文件夹下存放了sql命令。\

path: /db/migrations/001_20230215_2323/schema.sql

## 4 配置

/conf/config.json