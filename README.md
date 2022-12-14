# gasVyboryServer

# Сборка и запуск

```bash

docker build -t "server:latest" . --build-arg mongo_ip="0.0.0.0" --build-arg mongo_port="27017" --build-arg mongo_usr="admin" --build-arg mongo_pwd="admin" --build-arg kafka_port="9092"
    
docker run -e mongo_ip="0.0.0.0" -e mongo_port="27017" -e mongo_usr="admin" -e mongo_pwd="admin" -e kafka_port="9092" --expose=9092 server:latest

```
