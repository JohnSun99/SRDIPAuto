def fun_create_Vlan_Vni(int_Vlan, str_VlanName, int_Vni, int_DCN_AS):
        str_Vlan = str(int_Vlan)
        str_Vni = str(int_Vni)
        str_DCN_AS = str(int_DCN_AS)
	
# vlan    
        print("!")
        print("vlan", str_Vlan)
        if len(str_VlanName) > 32:
            print("!warning " + str_VlanName + "is too long >32")
        print("  name " + str_VlanName[0:32])    
        print("  vn-segment", str_Vni)
        print("!")              
# nve
        print("!")
        print("interface nve 1")
        print("  member vni", str_Vni)
        print("    mcast-group 239.0.0.1")
        print("!")        
# evpn
        print("!")
        print("evpn")
        print("  vni", str_Vni, "l2")
        print("    rd auto")
        print('    route-target both ' + str_DCN_AS +':' + str_Vni)
        print("!")


f = open('D:/eBook/Python/scripts/testcode/test_data2.csv', 'r')
for line in f:
        l_line = line.split(';')
        int_my_Vlan = int(l_line[0])
        int_my_Vni = int(l_line[1])
        str_my_VlanName = l_line[2]
        int_my_DCN_AS = 64522
        fun_create_Vlan_Vni(int_my_Vlan, str_my_VlanName, int_my_Vni, int_my_DCN_AS)
