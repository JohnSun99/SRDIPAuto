from iosswitchLite import *
from pprint import pprint
from collections import namedtuple
import csv
import datetime
import time


#	cbnb48g-01-c65dsa1	10.25.1.70
#	cbnb09i-h1-c65dsa1	10.23.1.70

# SAP_HANA_CBM
#	cbnb48g-gf-c65dsb1	10.30.5.6
#	cbnb09i-h1-c65dsc1	10.30.5.133

# Storage
#	cbnb09i-h1-c55asa1	10.30.5.29
#	cbnb09i-h1-c55asa2	10.30.5.30
#	cbnb48g-02-c55asa1	10.30.5.27
#	cbnb48g-02-c55asa2	10.30.5.28
#

while True:
	print '\n' * 2
	log_file = open('log-pre-dsa1.txt', "a+")
	currentTime = str(datetime.datetime.now())[0:16]
	s_print = '\n!!!!!!!!!!!!!  pre-change-Checking on cbnb48g-01-c65dsa1 at ' + currentTime
	print s_print
	log_file.write(s_print)
	switch1 = iosSwitch('10.25.1.70')
	
	d_mac_ip = {}
	Keys = namedtuple('cbnb48g_01_c65dsa1', 'Vlan_ID Mac_Add')
	
	currentTime = str(datetime.datetime.now())[0:16]
	
	with open("bwBurwest-mac-arp.csv", "rb") as infile:
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
	
	with open('bwBurwest-mac-arp.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerow(['Vlan_ID', 'MAC', 'IP', 'Intf', 'Time'])
		writer.writerows(ll_item)
		
######## Norwest dsa1   ================================================================
	print '\n' * 2
	currentTime = str(datetime.datetime.now())[0:16]
	s_print = '\n!!!!!!!!!!!!!  pre-change-Checking on cbnb09ir-h1-c65dsa1 at ' + currentTime
	print s_print
	log_file.write(s_print)

	switch1 = iosSwitch('10.23.1.70')
	
	d_mac_ip = {}
	Keys = namedtuple('cbnb09i_h1_c65dsa1', 'Vlan_ID Mac_Add')
	
	currentTime = str(datetime.datetime.now())[0:16]
	
	with open("nwBurwest-mac-arp.csv", "rb") as infile:
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
	
	with open('nwBurwest-mac-arp.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerow(['Vlan_ID', 'MAC', 'IP', 'Intf', 'Time'])
		writer.writerows(ll_item)
		
	log_file.close()		
	time.sleep(420)
