#!/bin/bash
while true
do
	CONN=$(docker exec $(docker ps --format '{{.Names}}' | grep $2) netstat -ant | grep -E ':80|:443' | wc -l)
	echo $CONN
	sleep $1
done