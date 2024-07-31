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

f = open('D:/eBook/Python/scripts/testcode/test_data1.csv', 'r')
d_input = {}
for line in f:
        l_line = line.split(';')
        s_host = l_line[0]
        s_intf = l_line[1]
        s_vlans = l_line[2].replace(' ','')
        l_vlans = fun_l_parse_vlans(s_vlans)
        s_desc = l_line[3]
        print (s_vlans)
        print (l_vlans)
