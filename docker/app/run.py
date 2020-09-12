#!/usr/bin/python
import os, string, random, time, socket, thread, sys, commands, json

def UDP_ECHO():
	while 1:
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			server = ('0.0.0.0', 733)
			sock.bind(server)
			print("Listening on 0.0.0.0:733")
			while True:
				payload, client_address = sock.recvfrom(8)
				print("Echoing data back to " + str(client_address))
				sent = sock.sendto(payload, client_address)
		except:
			print("Service stopped")
			time.sleep(2)

def EXEC(CMD):
	ERR_SUCCESS,OUTPUT = commands.getstatusoutput(CMD)
	return OUTPUT

#=====================================================

with open("/app/config", 'r') as f:
	CONF = json.loads(f.read())
print CONF
thread.start_new_thread(UDP_ECHO,())
while 1:
	CONNECTIONS = int(EXEC("docker exec $(docker ps --format '{{.Names}}' | grep '"+CONF['SERVICE']+"' | head -1) netstat -ant | grep -E ':80|:443' | wc -l"))
	print CONNECTIONS
	time.sleep(CONF['INTERVAL'])