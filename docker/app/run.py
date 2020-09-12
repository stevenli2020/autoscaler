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
REPLICATION = int(EXEC("docker service ps "+CONF['SERVICE']+" --format '{{.Name}}' | wc -l"))
# REPLICATION = REPLICATION + 2
# EXEC("docker service scale "+CONF['SERVICE']+"="+str(REPLICATION))
# exit()
PORTS = ""
for P in CONF['PORTS']:
	PORTS = PORTS+":"+str(P)+" |"
PORTS = PORTS[:-1]
print PORTS
T0 = time.time()-int(CONF['STABLIZATION'])
while 1:
	time.sleep(CONF['INTERVAL'])
	if CONF['MODE'] != "LEADER":
		if EXEC("echo -n '0' | nc -4u -w1 "+CONF['LEADER_NODE']+" 733") == "0":
			print "Leader node is online, skip"
			continue
	T1 = time.time()
	CONNECTIONS = int(EXEC("docker exec $(docker ps -f NAME=$(docker service ps -f NODE="+CONF['NODE']+" "+CONF['SERVICE']+" --format '{{.Name}}' | head -1) --format '{{.Names}}') netstat -tan | grep -E '"+PORTS+"' | wc -l"))
	print "Current number of containers: "+str(REPLICATION)+", connections on each: "+str(CONNECTIONS)
	if T1 - T0 > int(CONF['STABLIZATION']):
		if CONNECTIONS > CONF['CONN_THRESHOLD_H']:
			REPLICATION = REPLICATION + 2
			print "Scale up service '"+CONF['SERVICE']+"' by 2, REPLICATION="+str(REPLICATION)
			EXEC("docker service scale "+CONF['SERVICE']+"="+str(REPLICATION))
			print "Wait 30s for connection to be stablized..."
			T0 = time.time()			
		elif CONNECTIONS < CONF['CONN_THRESHOLD_L'] and REPLICATION != CONF['BASE_REPLICATION']:
			REPLICATION = REPLICATION - 2
			print "Scale down service '"+CONF['SERVICE']+"' by 2, REPLICATION="+str(REPLICATION)
			EXEC("docker service scale "+CONF['SERVICE']+"="+str(REPLICATION))
			print "Wait 30s for connection to be stablized..."
			T0 = time.time()
	
	
	
	
	
	
	