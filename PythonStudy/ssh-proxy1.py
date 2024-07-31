#!/usr/bin/env python 

import sys, paramiko 

hostname = "10.70.0.253"
password = "G89GaoXing"
command = "ls"
username = "d368451" 
port = 22 

try: 
	client = paramiko.SSHClient() 
	client.load_system_host_keys() 
	#client.set_missing_host_key_policy(paramiko.WarningPolicy())
      
	client.connect(hostname, port=port, username=username, password=password) 
 

	stdin, stdout, stderr = client.exec_command(command) 
	print (stdout.read())
 

finally: 
	client.close() 
