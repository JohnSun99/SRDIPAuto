def fun_int_My_AS(hostname):

	if hostname.count('48GE') > 0:
		int_AS = 64522
	elif hostname.count('09IR') > 0:
		int_AS = 64523
	else:
		int_AS = 99999
		
	return int_AS

host1 = 'CBPDCNCL-N09IR2C-RT05'
print(str(fun_int_My_AS(host1)))

