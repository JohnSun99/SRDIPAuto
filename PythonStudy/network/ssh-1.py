from netmiko import ConnectHandler

R1 = {
    'device_type': 'cisco_ios',
    'ip': '192.168.100.254',
    'username': 'cisco',
    'password': 'cisco',
}
R1_connect = ConnectHandler(**R1)
output = R1_connect.send_command('show ip int brief')
print(output)

config_commands = [ 'logging buffered 20000',
                    'logging buffered 20010',
                    'no logging console' ]
output = R1_connect.send_config_set(config_commands)
print(output)
