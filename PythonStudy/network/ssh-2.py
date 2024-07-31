from netmiko import ConnectHandler
from datetime import datetime

R1 = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.101.2',
    'username': 'cisco',
    'password': 'cisco',
    'verbose': False,
}

R2 = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.101.1',
    'username': 'cisco',
    'password': 'cisco',
    'verbose': False,
}

all_devices = [R1, R2]

start_time = datetime.now()
print (start_time)
for a_device in all_devices:
    net_connect = ConnectHandler(**a_device)
    output = net_connect.send_command("show arp")
    print ("\n\n>>>>>>>>>",net_connect.find_prompt(), "<<<<<<<<<")
    print (output)
    print (">>>>>>>>> End <<<<<<<<<")
end_time = datetime.now()
total_time = end_time - start_time 

print (end_time)
print ("total time is", total_time)
