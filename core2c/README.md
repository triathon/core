# Core2c

core 2c is a detection service
# CODE-SPECIFICATION

All instructions below are based on the premise that they are in the current folder

## 1 code
git: https://github.com/triathon/core

main: main-branch

code-folder: core2c
## 2 ENVIRONMENT_CONSTITUTION

create an image in the current directory
### 2.1 development environment construction

The dev.dockerfile in the folder is the docker image construction file of the development environment. After the image is built using this file, development tools can be used to develop the image in the container。

### 2.2 production environment construction

The Dockerfiles in the folder are docker image build files for the production environment

## 3 database
PostgreSQL 12.0 \
the sql commands are stored in the db folder。

path: /db/migrations/001_20230215_2323/schema.sql

## 4 configuration

/conf/conf.json