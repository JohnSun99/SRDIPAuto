# each line of csv file should looks like this "2;Inter-Distribution-Links"
def fun_d_vlanname_csv_to_dict(var_s_filename):
        f_vlanname_csv = open(var_s_filename, 'r')
        d_vlanname = {}
        for line in f_vlanname_csv:
                l_line = line.split(';')
                s_vlan = l_line[0]
                s_vlanname = l_line[1].replace('\n','')
        
                if s_vlan not in d_vlanname:
                    d_vlanname[s_vlan] = s_vlanname
                
        return d_vlanname
print(fun_d_vlanname_csv_to_dict('D:/eBook/Python/scripts/dcnDIP/BWIPNetVlanName.csv'))
