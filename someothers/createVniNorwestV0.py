# input is legacy vlan#, vlan name and vni#.

def createVni(vVlan, vVlanName, vVni):
# vlan    
    if vVni//1000 == 14 or 24 : # adjust vlan#based on vni#
        vVlan = vVlan + 1000
    print("vlan", vVlan)
    if len(vVlanName) > 32:
        print("!warning " + vVlanName + "is too long >32")
    print("  name" + vVlanName[0:32])    
    print("  vn-segment",vVni)
# nve
    print("interface nve 1")
    print("  member vni", vVni)
    print("    mcast-group 239.0.0.1")
# evpn
    print("evpn")
    print("  vni", vVni, "l2")
    print("    rd auto")
    print('    route-target both 64523:' + str(vVni))
    print()
        

f = open('D:/eBook/Python/vlans.txt', 'r')
for line in f:
    createVni(int(line.split()[0]), line.split()[1], int(line.split()[2]))
