def updateVni(vVlan):
    # delete the old vni
    vVni = 10000 + vVlan
    print("evpn")
    print("  no vni", vVni, "l2")
    print("interface nve 1")
    print("  no member vni", vVni)
    print("vlan", vVlan)
    print("  no vn-segment", vVni)
    # update with new VNIs
    vVni = 20000 + vVlan
    print("  vn-segment", vVni)
    print("interface nve 1")
    print("  member vni", vVni)
    print("    mcast-group 239.0.0.1")
    print("evpn")
    print("  vni", vVni, "l2")
    print("    rd auto")
    print('    route-target both 64522:' + str(vVni))
    print()
        

f = open('D:/eBook/Python/vlans.txt', 'r')
for line in f:
    updateVni(int(line))

