import csv
from sys import *
from pprint import pprint
from dcnswitch import *
import gen_funs
import random
import os


def check_os():
    print(os.getcwd())


def f_generate_vlan_vni(hostname, new_vlans):
    print >> f1, "!!!!!!!!! Creating-VLAN-VNI for host %s " % hostname
    i_my_AS = fun_int_My_AS(host_name)
    for each_new_vlan in new_vlans:
        fun_create_Vlan_Vni(each_new_vlan, i_my_AS)


def f_generate_port_common_1(switch_id, port_id, port_details):
    print >> f1, '!'
    if port_details['overwrite'] == 'yes':
        print >> f1, "default interface %s" % port_id
        print >> f1, '!'

    print >> f1, "interface %s" % port_id
    print >> f1, "  description %s " % port_details['desc']
    print >> f1, "  no cdp enable"
    print >> f1, "  switchport"
    if port_details['vpc'] != 0:
        print >> f1, "  channel-group %d mode active" % port_details['vpc']


def f_generate_port_common_2(port_id, port_details):
    if port_details['vpc'] == 0:
        if port_details['speed'] != 'auto':
            print >> f1, "  speed %s" % port_details['speed']

        if port_details['duplex'] != 'auto':
            print >> f1, "  duplex %s" % port_details['duplex']

        if port_details['vpc'] != 0:
            print >> f1, "  channel-group %s mode active" % str(
                port_details['vpc'])

        print >> f1, "  mtu %s" % str(port_details['mtu'])
        print >> f1, "  storm-control broadcast level 5.00"
    if port_details['shutdown'] == 'yes':
        print >> f1, "  shutdown"
    else:
        print >> f1, "  no shutdown"


def f_generate_port_access(port_details):
    print >> f1, "  switchport mode access"
    print >> f1, "  switchport access vlan %s" % str(port_details['vlans'][0])
    print >> f1, "  spanning-tree port type edge"


def f_generate_port_trunk(port_details):
    print >> f1, "  switchport mode trunk"
    print >> f1, "  switchport trunk native vlan 3965"
    # print >> f1, " !!!!!!!! Warning .... please double check if the port is being used, in case it is going to overwrite the vlan info"
    print >> f1, "  switchport trunk allowed vlan add %s" % str(
        port_details['vlans']).strip('[]')
    print >> f1, "  spanning-tree port type edge trunk"


def f_find_vpc_info(each_switch, each_vpc):
    for each_port in req[each_switch]:
        for port, port_details in each_port.items():
            if each_vpc == port_details['vpc']:
                return port_details


def f_generate_vpc(vpc_num, port_details):
    print >> f1, "interface port-channel %s" % str(vpc_num)
    print >> f1, "  description vPC %s " % str(vpc_num)
    if port_details['mode'] == 'access':
        f_generate_port_access(port_details)
    else:
        f_generate_port_trunk(port_details)
    if port_details['speed'] != 'auto':
        print >> f1, "  speed %s" % port_details['speed']

    if port_details['duplex'] != 'auto':
        print >> f1, "  duplex %s" % port_details['duplex']
    print >> f1, "  storm-control broadcast level 5.00"
    print >> f1, "  mtu %s" % str(port_details['mtu'])
    print >> f1, "  vpc %s " % str(vpc_num)
    print >> f1, "!"


def fun_int_My_AS(hostname):
    if hostname.count('48GE') > 0:
        int_AS = 64522
    elif hostname.count('09IR') > 0:
        int_AS = 64523
    else:
        int_AS = 99999
    return int_AS


def fun_create_Vlan_Vni(v_i_Vlan, v_i_DCN_AS):

    s_Vlan = str(v_i_Vlan)
    # Burwest vlan migration 1-999
    if v_i_Vlan < 1000:
        i_Vni = 10000 + v_i_Vlan
        # print(s_Vlan)
        if v_i_Vlan in d_Burwest_vlanname.keys():
            s_VlanName = d_Burwest_vlanname[v_i_Vlan]['vlan_name']
        else:
            print "! Warning!!! " + s_Vlan + " does not existing on Burwest network"
            return ()
    # Norwest IPNet vlan migration 1xxx
    elif ((v_i_DCN_AS == 64523) and (v_i_Vlan < 2000)):
        i_Vni = 13000 + v_i_Vlan
        if v_i_Vlan - 1000 in d_NWIPNet_vlanname.keys():
            s_VlanName = d_NWIPNet_vlanname[v_i_Vlan - 1000]['vlan_name']
        else:
            print "! Warning!!! " + s_Vlan + " does not existing on Norwest IPNet"
            return ()
    # Burwood IPNet vlan migration 1xxx
    elif ((v_i_DCN_AS == 64522) and (v_i_Vlan < 2000)):
        i_Vni = 10000 + v_i_Vlan
        if v_i_Vlan - 1000 in d_BWIPNet_vlanname.keys():
            s_VlanName = d_BWIPNet_vlanname[v_i_Vlan - 1000]['vlan_name']
        else:
            print "! Warning!!! " + s_Vlan + " does not existing on Burwood IPNet"
            return ()
    # Burwood new vlans 2xxx and Norwest new vlans 3xxx
    else:
        i_Vni = 10000 + v_i_Vlan
        s_VlanName = "new_Vlan_need_mannual"
    s_Vni = str(i_Vni)
    s_DCN_AS = str(v_i_DCN_AS)


# vlan
    print >> f1, "!"
    print >> f1, "vlan " + s_Vlan
    if len(s_VlanName) > 32:
        print("!warning " + s_VlanName + "is too long >32")
    print >> f1, "  name " + s_VlanName[0:32]
    print >> f1, "  vn-segment " + s_Vni
    print >> f1, "!"
# nve
    print >> f1, "!"
    print >> f1, "interface nve 1"
    print >> f1, "  member vni " + s_Vni
    print >> f1, "    mcast-group 239.0.0.1"
    print >> f1, "!"
# evpn
    print >> f1, "!"
    print >> f1, "evpn"
    print >> f1, "  vni " + s_Vni + " l2"
    print >> f1, "    rd auto"
    print >> f1, '    route-target both ' + s_DCN_AS + ':' + s_Vni
    print >> f1, "!"


# main() start here
if len(argv) <= 1:
    print 'format is: python3 dipauto.py req_csv yourname'
    exit()

d_host_ip = gen_funs.d_read_host_file()
# print '\n d_host_ip'
# pprint(d_host_ip)

# read in uni requirement details from req_csv file
d_uni_req = gen_funs.d_read_uni_req(argv[1])
# print '\n d_uni_req'
# pprint(d_uni_req)

# find vpc required for each switch and put it into a dictinary d_req_vPCs
d_req_vPCs = gen_funs.d_get_switch_vPC_list(d_uni_req)
# print '\n d_req_vPCs'
# pprint(d_req_vPCs)

# find vlans requried for each switch and put it into a dictionary d_req_vlans
d_req_vlans = gen_funs.d_get_switch_req_vlan_list(d_uni_req)
# print '\n d_req_vlans'
# pprint(d_req_vlans)

# create MLs to access its vlan/vxlan info
bwIPNetML = DCNSwitch('10.88.0.79')
nwIPNetML = DCNSwitch('10.89.0.79')
BurwestML1 = DCNSwitch('10.88.0.81')
BurwestML2 = DCNSwitch('10.88.0.83')

d_Burwest_vlanname = BurwestML1.vlans
d_Burwest_vlanname.update(BurwestML2.vlans)
d_BWIPNet_vlanname = bwIPNetML.vlans
d_NWIPNet_vlanname = nwIPNetML.vlans

# creat a switch object for each switch, put it into a dictionary and then check the port status of each port in REQ
d_switches = {}
d_switches_configured_ports = {}
for host_name, port_list in d_uni_req.items():
    d_switches[host_name] = DCNSwitch(d_host_ip[host_name])
    # d_switches_configured_ports[host_name]
    d_configured_ports = d_switches[host_name].check_ports_status(port_list)
    for each_port in port_list:
        for port_ID, d_port_req_details in each_port.items():
            if port_ID in d_configured_ports.keys():
                d_port_req_details['configured'] = d_configured_ports[port_ID]['configured']
                d_port_req_details['running_config'] = d_configured_ports[port_ID]['running_config']
                d_port_req_details['up'] = d_configured_ports[port_ID]['up']
                if d_port_req_details['up'] == 'yes':
                    print '\n' * 3
                    print 'Warning!!! Critical !!!' + host_name + ' ' + port_ID + ' is UP, What the hell!'
                    print 'configuration for the port will NOT be generated!!!! Please manually configure yourself!!!!'
                    continue
                    # exit()
                if d_port_req_details['overwrite'] != 'yes':
                    print '\n' * 2
                    print 'Warning!!! ' + host_name + ' ' + port_ID + ' is configured, but did NOT ask for overwriting, please double check '
                    pprint(d_port_req_details['running_config'])
                    while True:
                        random_number = int(random.uniform(100, 999))
                        s_random_number = str(random_number)
                        print 'Do you want to overwrite the port configuration and continue?'
                        input_message = " type '" + s_random_number + "' for yes, or type '000' to exit:"
                        try:
                            your_input = input(input_message)
                        except:
                            continue
                        s_your_input = str(your_input)
                        s_no = str(000)
                        if s_your_input == s_random_number:
                            d_port_req_details['overwrite'] = 'yes'
                            break
                        elif s_your_input == s_no:
                            exit()
                        else:
                            print s_your_input + ' is NOT a valid input'
            else:
                d_port_req_details['configured'] = 'no'
                d_port_req_details['running_config'] = []
                d_port_req_details['up'] = 'no'
# pprint(d_uni_req)

# find peer for each switch and put it into a dictionary
d_peers = {}
for each_switch in d_req_vlans.keys():
    if each_switch not in d_peers.keys():
        d_peers[each_switch] = d_switches[each_switch].peer
# print '\n d_peers'
# pprint(d_peers)

d_peer_req_vlans = gen_funs.d_get_peer_req_vlan_list(d_peers, d_req_vlans)
# print '\n d_peer_req_vlans'
# pprint(d_peer_req_vlans)

# now, let's find the new vlans for each switch pair
d_peer_req_new_vlans = {}
for each_switch, sw_pair_req_vlans in d_peer_req_vlans.items():
    d_peer_req_new_vlans[each_switch] = []
    current_vlans = d_switches[each_switch].vlans.keys()
    for each_vlan in sw_pair_req_vlans:
        if each_vlan not in current_vlans:
            d_peer_req_new_vlans[each_switch].append(each_vlan)
# print '\n d_peer_req_new_vlans'
# pprint(d_peer_req_new_vlans)

f1 = open('test.txt', "w+")

# !!!! Good, let's generate the configuration now ......
for each_switch, port_list in d_uni_req.items():
    # we need get vlan-vni 1st....
    if len(argv) <= 2:
        f1 = open(argv[1].split('.')[0] + '-' + each_switch + '.txt', "w+")
    else:
        f1 = open(argv[2] + '-' + argv[1].split('.')
                  [0] + '-' + each_switch + '.txt', "w+")
    print >> f1, '\n' * 2

    if d_switches[each_switch].role == 'NC':
        print >> f1, '!! Login to switch %s and its peer switch %s' % (
            each_switch, d_peers[each_switch])
    else:
        print >> f1, '!! Login to switch %s' % each_switch

    print >> f1, 'conf t'
    new_vlans = d_peer_req_new_vlans[each_switch]
    if len(new_vlans) > 0:
        f_generate_vlan_vni(each_switch, new_vlans)

    for each_port in port_list:
        for port_id, port_details in each_port.items():
            if port_details['up'] == 'yes':
                print 'Warning!!! Skipping generating configuration for up port ' + each_switch + ' ' + port_id
                continue
            f_generate_port_common_1(each_switch, port_id, port_details)
            if port_details['vpc'] == 0:
                if port_details['mode'] == 'access':
                    f_generate_port_access(port_details)
                else:
                    f_generate_port_trunk(port_details)
            f_generate_port_common_2(port_id, port_details)
    # print >> f1, '\n' * 2
    temp_vPCs = d_req_vPCs[each_switch]
    if len(temp_vPCs) > 0:
        for each_vpc in temp_vPCs:
            vpc_port_details = f_find_vpc_info(each_switch, each_vpc)
            f_generate_vpc(each_vpc, vpc_port_details)

    print >> f1, 'end'
    d_switches[each_switch].connect_close()
    f1.close()
