from bluetooth import *

print "performing inquiry"

nearby_devices = discover_devices(lookup_names = True)

print "found %d devices" %len(nearby_devices)

for name in nearby_devices:
	print "%s -%s" % (name)

#hardcode phone macaddr
phone = "C4:93:D9:AE:63:4B"

#split tuple so we get just the mac addr
(addr, ownder) = name

if addr == phone:
	print("match found")





