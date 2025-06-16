#!/bin/bash
docker stop ia; docker rm ia
( cd ia; docker build --rm -t ia . )
docker stop app; docker rm app
( cd app; mvn clean package -DskipTests; docker build --rm -t app . )
