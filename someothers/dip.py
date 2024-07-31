def fun_l_parse_vlans(var_s_vlans):
        l_all_vlans = []
        l_vlan_comma = var_s_vlans.split(',')
        for entry in l_vlan_comma:
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

# each line of csv file should looks like this "CBPDCNCL-N48GE2B-RT05;Eth1/8;1901;SLAC-UPM-bh2-i21-843D1EW-HMC Port 1"
#                                           or "CBPDCNFL-N48GE2C-RT05;E1/13;40,42,308,310,311,324,325,327,415-425,436-445,456-465,507,508,821,822;SLAC-UDD-viobwh3e812n-CEC 4 P1-C2-C1-T1"
def fun_d_port_csv_to_dict(var_s_filename):
        s_full_filename = var_s_filename.replace('\\','\/')
        f_port_csv = open(s_full_filename, 'r')
        d_input = {}
        l_port = []
        for line in f_port_csv:
                l_line = line.split(';')
                s_host = l_line[0]
                s_intf = l_line[1]
                s_vlans = l_line[2].replace(' ','')
                l_vlans = fun_l_parse_vlans(s_vlans)
                s_desc = l_line[3].replace('\n','')
                l_port = [s_intf, l_vlans, s_desc]
        
                if s_host not in d_input:
                        #print("new host %s" % s_host)
                        d_input[s_host] = []
                d_input[s_host].append(l_port)
        return d_input


d_portInfo = fun_d_port_csv_to_dict('D:\eBook\Python/scripts/testcode/test_data11.csv')
print (d_portInfo)

#for key,vlaue in d_portInfo
