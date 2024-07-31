host = "10.70.0.253"
user = "d368451"
#passwd = "Jhwsx168"

def main():
	# Prompt for a password instead of embedding it in a script...
	#
	passwd = crt.Dialog.Prompt("Enter password for " + host, "Login", "", True)

	# Build a command-line string to pass to the Connect method.
	cmd = "/SSH2 /L %s /PASSWORD %s /C 3DES /M MD5 %s" % (user, passwd, host)
	crt.Session.Connect(cmd)


main()
