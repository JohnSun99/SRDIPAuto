[root@CBPDCNMG-N48GE2B-SR01-DCNM v11]# cat evpn.py 
from dcnswitchLite import *
import gen_funs
from pprint import pprint


d_host_ip = gen_funs.d_read_host_file()
l_uptime = open('uptime.txt', 'r')

for line in l_uptime:
    switch1 = DCNSwitch(d_host_ip[line.strip('\n')])
    cli = "show system uptime | i start"
    output = switch1.general_check(cli)
    #print '\n' * 2
    print line.strip('\n') + ': ' + str(output[0])
    #pprint(output)
[root@CBPDCNMG-N48GE2B-SR01-DCNM v11]# 