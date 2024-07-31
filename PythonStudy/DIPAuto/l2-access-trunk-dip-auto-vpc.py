# source files required:
# 1 "D:/PythonStudy/DIPAuto/data/REQxxxxxx.csv   ================== each new SR
s_REQ_full_filename = "D:/PythonStudy/DIPAuto/data/RITM-REQ1431556-lit.csv"

# 2 "D:/PythonStudy/DIPAuto/data/" + switch-hostname + "-vlans.txt"  ================= every Leaf pair need current vlans by logging switches "show vxlan" and take the vlans
#


# static source file:
# "D:/PythonStudy/DIPAuto/data/Leaf-peer.csv"   =================== need update if new switches PoAPed
# "D:/PythonStudy/DIPAuto/data/BurWestVlanName.csv"
# "D:/PythonStudy/DIPAuto/data/BWIPNetVlanName.csv"
# "D:/PythonStudy/DIPAuto/data/NWIPNetVlanName.csv"



def fun_csv_to_dict(v_s_full_filename):
        d_output = {}
        with open(v_s_full_filename) as f_csv_file:
                for s_each_line in f_csv_file:
                        (key, val) = s_each_line.split(";")
                        d_output[key.strip()] = val.strip()
        f_csv_file.close()
        return(d_output)

def fun_csv_to_i_list(v_s_full_filename):
        d_output = []
        with open(v_s_full_filename) as f_csv_file:
                for s_each_line in f_csv_file:
                        d_output.extend([int(s_each_line.strip())])
        f_csv_file.close()
        return(d_output)

def fun_csv_to_s_list(v_s_full_filename):
        d_output = []
        with open(v_s_full_filename) as f_csv_file:
                for s_each_line in f_csv_file:
                        d_output.extend([s_each_line.strip('\n')])
        f_csv_file.close()
        return(d_output)

def fun_create_Vlan_Vni(v_i_Vlan, v_i_DCN_AS):
        d_Burwest_vlanname = fun_csv_to_dict("D:/PythonStudy/DIPAuto/data/BurWestVlanName.csv")
        d_BWIPNet_vlanname = fun_csv_to_dict("D:/PythonStudy/DIPAuto/data/BWIPNetVlanName.csv")
        d_NWIPNet_vlanname = fun_csv_to_dict("D:/PythonStudy/DIPAuto/data/NWIPNetVlanName.csv")
        
        s_Vlan = str(v_i_Vlan)
        # Burwest vlan migration 1-999
        if v_i_Vlan < 1000:
                i_Vni = 10000 + v_i_Vlan
                #print(s_Vlan)
                s_VlanName = d_Burwest_vlanname[s_Vlan]
        # Norwest IPNet vlan migration 1xxx
        elif ((v_i_DCN_AS == 64523) and (v_i_Vlan < 2000)):
                i_Vni = 13000 + v_i_Vlan
                #print(s_Vlan, i_Vni)
                #s_VlanName = "test"
                s_VlanName = d_NWIPNet_vlanname[s_Vlan]
        # Burwood IPNet vlan migration 1xxx                
        elif ((v_i_DCN_AS == 64522) and (v_i_Vlan < 2000)):
                i_Vni = 10000 + v_i_Vlan
                s_VlanName = d_BWIPNet_vlanname[s_Vlan]
        # Burwood new vlans 2xxx and Norwest new vlans 3xxx
        else:
                i_Vni = 10000 + v_i_Vlan
                s_VlanName = "new_Vlan_need_mannual"
        s_Vni = str(i_Vni)
        s_DCN_AS = str(v_i_DCN_AS)
	
# vlan    
        print("!")
        print("vlan", s_Vlan)
        if len(s_VlanName) > 32:
            print("!warning " + s_VlanName + "is too long >32")
        print("  name " + s_VlanName[0:32])    
        print("  vn-segment", s_Vni)
        print("!")              
# nve
        print("!")
        print("interface nve 1")
        print("  member vni", s_Vni)
        print("    mcast-group 239.0.0.1")
        print("!")        
# evpn
        print("!")
        print("evpn")
        print("  vni", s_Vni, "l2")
        print("    rd auto")
        print('    route-target both ' + s_DCN_AS +':' + s_Vni)
        print("!")


def fun_backout_Vlan_Vni(v_i_Vlan, v_i_DCN_AS):
        
        s_Vlan = str(v_i_Vlan)         
        if v_i_Vlan < 1000:
                i_Vni = 10000 + v_i_Vlan
        elif (v_i_DCN_AS == 64523) and (v_i_Vlan < 2000):
                i_Vni = 13000 + v_i_Vlan
        else:
                i_Vni = 10000 + v_i_Vlan
                    
        s_Vni = str(i_Vni)

# evpn
        print("!")
        print("evpn")
        print("  no vni", s_Vni, "l2")
        print("!")
     
# nve
        print("!")
        print("interface nve 1")
        print("  no member vni", s_Vni)
        print("!")        

# vlan    
        print("!")
        print("no vlan", s_Vlan)
        print("!")  


def fun_int_My_AS(hostname):
	if hostname.count('48GE') > 0:
		int_AS = 64522
	elif hostname.count('09IR') > 0:
		int_AS = 64523
	else:
		int_AS = 99999
		
	return int_AS
	
def fun_d_port_csv_to_dict(var_s_filename):
        f_port_csv = open(var_s_filename, 'r')
        d_output = {}
        l_port = []
        for line in f_port_csv:
                l_line = line.split(';')
                s_host = l_line[0]
                s_intf = l_line[1]
                s_vlans = l_line[2].replace(' ','')
                #l_vlans = fun_l_parse_vlans(s_vlans)
                s_desc = l_line[3].replace('\n','')
                l_port = [s_intf, s_vlans, s_desc]
        
                if s_host not in d_output:
                        #print("new host %s" % s_host)
                        d_output[s_host] = []
                d_output[s_host].append(l_port)
        return d_output


def fun_l_parse_vlans(var_s_vlans):
        l_all_vlans = []
        l_vlan_comma = var_s_vlans.split(',')
        for entry in l_vlan_comma:
                #print(entry)
                if '-' in entry:
                        l_group_vlan = entry.split('-')
                        i_begin_vlan = int(l_group_vlan[0])
                        i_end_vlan = int(l_group_vlan[1])
                        while i_begin_vlan <= i_end_vlan:
                                if l_all_vlans.count(i_begin_vlan)==0:
                                        l_all_vlans.extend([i_begin_vlan])
                                i_begin_vlan = i_begin_vlan + 1
                else:
                        i_begin_vlan = int(entry)
                        if l_all_vlans.count(i_begin_vlan)==0:
                                l_all_vlans.extend([i_begin_vlan])
                
        l_all_vlans = sorted(l_all_vlans, key=int)
        return l_all_vlans

# main() start here

# step1: put the leaf peers into a dictionary
d_peer = fun_csv_to_dict("D:/PythonStudy/DIPAuto/data/Leaf-peer.csv")

# step2: collect all requried vlans for each leaf pair and put into a dictionary
# ???? 
f_req = open(s_REQ_full_filename, 'r')

d_host_vlans = {}
for line in f_req:
        l_line = line.split(';')
        #print(l_line)
        #print (d_peer)
        s_host = d_peer[l_line[0].strip()].strip('\n')
        s_vlans = l_line[2].strip()
        l_vlans = fun_l_parse_vlans(s_vlans)
        #print (s_host)
        #print (s_vlans)
        #print (l_vlans)
        if s_host not in d_host_vlans:
                d_host_vlans[s_host] = []
        for i_vlan in l_vlans:
                if i_vlan not in d_host_vlans[s_host]:
                        d_host_vlans[s_host].extend([i_vlan])
        d_host_vlans[s_host] = sorted(d_host_vlans[s_host], key=int)
#print(d_host_vlans)

# step3: put existing vlans of each peer pair into a list and then find out the new vlans by comparing to all required vlans
# then Creating-VLAN-VNI for each leaf pair
l_host_vlans_now = []
d_host_new_vlans = {}
for key, value in d_host_vlans.items():
        s_host_vlan_file = "D:/PythonStudy/DIPAuto/data/" + key + "-vlans.txt"
        print (s_host_vlan_file)
        #print("required vlan number is %d" % len(value))
        l_host_vlans_now = fun_csv_to_i_list(s_host_vlan_file)
        l_new_vlans = [ x for x in value if x not in l_host_vlans_now]
        #print("existing vlans on %s" % s_host)
        #print(l_host_vlans_now)
        #print("requried new %d vlans are ..............." % len(l_new_vlans))
        #print(l_new_vlans)
        d_host_new_vlans[key] = l_new_vlans
        print("!!!!!!!!! Creating-VLAN-VNI for host %s and its peer" % key)
        i_my_AS = fun_int_My_AS(key)
        for s_each_new_vlan in l_new_vlans:
                fun_create_Vlan_Vni(int(s_each_new_vlan), i_my_AS)
#print(d_host_new_vlans)
for key, value in d_host_new_vlans.items():
        print("!!!!!!! Creating-backout-VLAN-VNI for host %s and its peer" % key)
        i_my_AS = fun_int_My_AS(key)
        for each_new_vlan in value:
                fun_backout_Vlan_Vni(each_new_vlan, i_my_AS)

# Step 4, Creating-port-configuration for each leaf switch
d_full_port_config_req = fun_d_port_csv_to_dict(s_REQ_full_filename)
# print(d_full_port_config_req)

for key, value in d_full_port_config_req.items():
        print ("!!!!!!!!! creating-port-configuration for %s" % key )
        for each_port in value:
                if len(fun_l_parse_vlans(each_port[1])) == 1:
                        # access port
                        print("interface %s" % each_port[0])
                        print("  description %s " % each_port[2])
                        print("  no cdp enable")
                        print("  switchport")
                        print("  switchport mode access")
                        print("  switchport access vlan %s" % each_port[1])
                        print("  mtu 9216")
                        print("  speed 1000")
                        print("  duplex full")
                        print("  spanning-tree port type edge")
                        print("  storm-control broadcast level 5.00")
                        
                        ports = each_port[0].split('/')
                        i_ports = int(ports[1])                        
                        print("  channel-group %s mode active" % str(200 + i_ports))
                        
                        print("  shutdown")
                        print("!")

                        print("interface port-channel %s" % str(200 + i_ports))
                        print("  description %s " % each_port[2])
                        print("  switchport")
                        print("  switchport mode access")
                        print("  switchport access vlan %s" % each_port[1])
                        print("  mtu 9216")
                        print("  storm-control broadcast level 5.00")                        
                        print("  vpc %s " % str(200 + i_ports))
                        print("!")
                else:
                        # trunk port
                        print("interface %s" % each_port[0])
                        print("  description %s " % each_port[2])
                        print("  no cdp enable")
                        print("  switchport")
                        print("  switchport mode trunk")
                        print("  switchport trunk native vlan 3965")
                        #print(" !!!!!!!! Warning .... please double check if the port is being used, in case it is going to overwrite the vlan info")
                        print("  switchport trunk allowed vlan %s" % each_port[1])
                        print("  spanning-tree port type edge trunk")
                        print("  mtu 9216")
                        print("  speed 1000")
                        print("  duplex full")                        
                        print("  storm-control broadcast level 5.00")
                        ports = each_port[0].split('/')
                        i_ports = int(ports[1])                        
                        print("  channel-group %s mode active" % str(200 + i_ports))
                        print("  shutdown")
                        print("!")

                        print("interface port-channel %s" % str(200 + i_ports))
                        print("  description %s " % each_port[2])
                        print("  switchport")
                        print("  switchport mode trunk")
                        print("  switchport trunk native vlan 3965")
                        print("  switchport trunk allowed vlan %s" % each_port[1])
                        print("  spanning-tree port type edge trunk")
                        print("  mtu 9216")
                        print("  storm-control broadcast level 5.00")
                        print("  vpc %s " % str(200 + i_ports))
                        print("!")
                        
f_req.close()



for key, value in d_full_port_config_req.items():
        print ("!!!!!!!!! creating-backout-port-configuration for %s" % key )
        for each_port in value:
                print("default interface %s" % each_port[0])
