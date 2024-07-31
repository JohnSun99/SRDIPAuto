import netmiko
import os


class CiscoIOS():

    def __init__(self, ip, port=22, prompt=False, username=None, password=None, device_type='cisco_ios'):
	    self.conn = netmiko.ConnectHandler(ip=ip, port=port, username=username, password=password, device_type=device_type)
        _ = self.conn.send_command('show run | in hostname')
        self.hostname = _.split()[-1]

    def get_run_cfg(self):
	    running_config = self.conn.send_command('show run')
        return running_config
		
    def get_ip_int(self):
	    ip_int = self.conn.send_command('show ip int')
        return ip_int
		
    def get_log(self):
	    log = self.conn.send_command("show log')
		return log
		
def main():
    ip_list = [
	    '10.254.0.1',
		'10.254.0.2',
		'10.254.0.3',
	]
	router_list = []
	
	for ip in ip_list:
	    conn = CiscoIOS(ip, username='cisco', password='cisco')
		router_list.append(conn)			
    for router in router_list:
	    base_dir = os.getcwd() + '/routers/'
		router_dir = base_dir + router.hostname + '/'
		os.mkdir(router_dir)
		data_dict = {
		    "running_config": router.get_run_cfg(),
			"ip-interface":router.get_ip_int(),
			"log":router.get_log(),
		}
		for output in data_dict:
		    filename = router_dir + output + '.txt'
			with open(filename, 'w') as f:
			    print(data_dict[output], file=f)

    for _ in os.walk('router'):
	    print(_)

if __name__ == '__main__':
    main()