def createVni(vVlan):
    #print("vlan", vVlan)
    vVni = 14000 + vVlan
    #print("  vn-segment",vVni)
    print("interface nve1")
    print("  member vni", vVni)
    print("    mcast-group 239.0.0.1")
    print("evpn")
    print("  vni", vVni, "l2")
    print("    rd auto")
    print('    route-target both 64523:' + str(vVni))
    print()
        

f = open('D:/eBook/Python/vlans.txt', 'r')
for line in f:
    createVni(int(line))

