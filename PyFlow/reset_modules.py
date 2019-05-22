import sys
sms=sys.modules.keys()
for m in sms:

	if m.startswith('PyFlow'):
		print m
		del(sys.modules[m])
