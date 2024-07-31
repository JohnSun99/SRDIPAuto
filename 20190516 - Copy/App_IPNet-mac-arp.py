from iosswitchLite import *
from pprint import pprint
from collections import namedtuple
import csv
import datetime
import time

#cbn48ge-01-c65ds01       10.25.0.3       
#cbn48ge-01-c65ds02       10.25.0.4 
#cbn09ir-h1-c65ds01       10.23.0.3       
#cbn09ir-h2-c65ds01       10.23.0.4       
  

while True:
	print '\n' * 2
	log_file = open('log-pre-IPNet.txt', "a+")
	currentTime = str(datetime.datetime.now())[0:16]
	s_print = '\n!!!!!!!!!!!!!  pre-change-Checking on cbn48ge-01-c65ds01 and ds02 at ' + currentTime
	print s_print
	log_file.write(s_print)
	switch1 = iosSwitch('10.25.0.3')
	switch2 = iosSwitch('10.25.0.4')
	
	d_mac_ip = {}
	Keys = namedtuple('vlan_mac', 'Vlan_ID Mac_Add')
	
	currentTime = str(datetime.datetime.now())[0:16]
	
	with open("bwIPNet-mac-arp.csv", "rb") as infile:
		reader = csv.reader(infile)
		next(reader, None)  # skip the headers
		for row in reader:
			vlanID = int(row[0])
			Mac = row[1]
			key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
			if key1 not in d_mac_ip:
				d_mac_ip[key1] = {}
				d_mac_ip[key1]["IP"] = row[2]
				d_mac_ip[key1]["Intf"] = row[3]
				d_mac_ip[key1]["Time"] = row[4]
	
	cli = "show mac address-table | i Yes"
	output = switch1.general_check(cli)
	output2 = switch2.general_check(cli)
	output.extend(output2)
	
	for each_item in output:
		each_mac = str(each_item)
		vlanID = int(each_mac[3:6].strip(' '))
		Mac = each_mac[8:22]
		Intf = each_mac[51:].strip('\n').strip('\r')
		key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
		#pprint(key1)
		if key1 not in d_mac_ip:
			d_mac_ip[key1] = {}
			d_mac_ip[key1]["Intf"] = Intf
			d_mac_ip[key1]["Time"] = currentTime      
			
	cli = "show ip arp | i Vlan"
	output = switch1.general_check(cli)
	
	for each_item in output:
		each_arp = str(each_item).strip('\n').strip('\r')
		s_vlanID = each_arp[65:]
		vlanID = int(s_vlanID)
		Mac = each_arp[38:52]
		IP = each_arp[10:30].strip(' ')
		key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
		#pprint(key1)
		if key1 in d_mac_ip:
			d_mac_ip[key1]["IP"] = IP
	#pprint(d_mac_ip)
	
	ll_item = []
	for key in sorted(d_mac_ip):
		#pprint (key)
		l_item = []
		l_item.append(key.Vlan_ID)
		l_item.append(key.Mac_Add)
		try:
			l_item.append(d_mac_ip[key]['IP'])
		except:
			l_item.append('No_IP')
		l_item.append(d_mac_ip[key]['Intf'])
		l_item.append(d_mac_ip[key]['Time'])
		ll_item.append(l_item)
        
	s_print = '  and it has ' + str(len(ll_item)) + ' MAC entries learn from Norwest at ' + currentTime
	print s_print
	log_file.write(s_print)

	#pprint(ll_item)
	
	with open('bwIPNet-mac-arp.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerow(['Vlan_ID', 'MAC', 'IP', 'Intf', 'Time'])
		writer.writerows(ll_item)
		
######## Norwest IPNet DS   ================================================================
	print '\n' * 2
	currentTime = str(datetime.datetime.now())[0:16]
	s_print = '\n!!!!!!!!!!!!!  pre-change-Checking on cbn09ir-h1-c65ds01 and 02 at ' + currentTime
	print s_print
	log_file.write(s_print)

	switch1 = iosSwitch('10.23.0.3')
	switch2 = iosSwitch('10.23.0.4')
	
	d_mac_ip = {}
	Keys = namedtuple('vlan_mac', 'Vlan_ID Mac_Add')
	
	currentTime = str(datetime.datetime.now())[0:16]
	
	with open("nwIPNet-mac-arp.csv", "rb") as infile:
		reader = csv.reader(infile)
		next(reader, None)  # skip the headers
		for row in reader:
			vlanID = int(row[0])
			Mac = row[1]
			key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
			if key1 not in d_mac_ip:
				d_mac_ip[key1] = {}
				d_mac_ip[key1]["IP"] = row[2]
				d_mac_ip[key1]["Intf"] = row[3]
				d_mac_ip[key1]["Time"] = row[4]
	
	cli = "show mac address-table | i Yes"
	output = switch1.general_check(cli)
	output2 = switch2.general_check(cli)
	output.extend(output2)
	
	for each_item in output:
		each_mac = str(each_item)
		vlanID = int(each_mac[3:6].strip(' '))
		Mac = each_mac[8:22]
		Intf = each_mac[51:].strip('\n').strip('\r')
		key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
		#pprint(key1)
		if key1 not in d_mac_ip:
			d_mac_ip[key1] = {}
			d_mac_ip[key1]["Intf"] = Intf
			d_mac_ip[key1]["Time"] = currentTime      
			
	cli = "show ip arp | i Vlan"
	output = switch1.general_check(cli)
	
	for each_item in output:
		each_arp = str(each_item).strip('\n').strip('\r')
		s_vlanID = each_arp[65:]
		vlanID = int(s_vlanID)
		Mac = each_arp[38:52]
		IP = each_arp[10:30].strip(' ')
		key1 = Keys(Vlan_ID=vlanID, Mac_Add=Mac)
		#pprint(key1)
		if key1 in d_mac_ip:
			d_mac_ip[key1]["IP"] = IP
	#pprint(d_mac_ip)
	
	ll_item = []
	for key in sorted(d_mac_ip):
		#pprint (key)
		l_item = []
		l_item.append(key.Vlan_ID)
		l_item.append(key.Mac_Add)
		try:
			l_item.append(d_mac_ip[key]['IP'])
		except:
			l_item.append('No_IP')
		l_item.append(d_mac_ip[key]['Intf'])
		l_item.append(d_mac_ip[key]['Time'])
		ll_item.append(l_item)
		
	s_print = ' and it has ' + str(len(ll_item)) + ' MAC entries learn from Burwood at ' + currentTime
	print s_print
	log_file.write(s_print)

	#pprint(ll_item)
	
	with open('nwIPNet-mac-arp.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerow(['Vlan_ID', 'MAC', 'IP', 'Intf', 'Time'])
		writer.writerows(ll_item)
		
	log_file.close()		
	time.sleep(420)
