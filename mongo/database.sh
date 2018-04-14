#!/usr/bin/env bash

if [ $1 == "restart" ] || [ $1 == "shutdown" ];
then
    # "C:/Program Files/MongoDB/Server/3.6/bin/mongod" --shutdown
    echo "shutting down database"
fi

if [ $1 == "start" ] || [ $1 == "restart" ];
then
    "C:/Program Files/MongoDB/Server/3.6/bin/mongod" --config C:/LITTLE_BIG_POND/mongo/mongod.conf
    echo "starting up database"
fi