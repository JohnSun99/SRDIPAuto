def noVlan(vVlan):
    vVni = 20000 + vVlan
    print("evpn")
    print("  no vni", vVni, "l2")
    print("interface nve 1")
    print("  no member vni", vVni)
    print("vlan", vVlan)
    print("  no vn-segment", vVni)
