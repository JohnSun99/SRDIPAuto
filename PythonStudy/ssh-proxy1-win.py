from netmiko import ConnectHandler
import time
from netmiko import redispatch

jumpserver = {'device_type': 'terminal_server','ip': '10.70.0.253','username': 'd368451','password': 'G89GaoXing','global_delay_factor':5}

net_connect = ConnectHandler(**jumpserver)
print (net_connect.find_prompt())


net_connect.

net_connect.write_channel('ssh 10.228.13.5')
output = net_connect.read_channel()
print(output)
time.sleep(5)
net_connect.write_channel('G89GaoXing')

redispatch(net_connect, device_type='cisco_ios')

time.sleep(5)
output = net_connect.send_command('show version | i uptime')
print(output)

