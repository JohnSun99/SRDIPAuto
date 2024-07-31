import paramiko

ip_address = '10.88.0.85'
username = 'ACOE-DCN_P_DCNM'
password = '21588Sp5520A7315'

print '\n------------------------------------------------------'
print '--- Attempting paramiko connection to: ', ip_address

# Create paramiko session
ssh_client = paramiko.SSHClient()

# Must set missing host key policy since we don't have the SSH key
# stored in the 'known_hosts' file
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Make the connection to our host.
ssh_client.connect(hostname=ip_address,
                   username=username,
                   password=password)

# If there is an issue, paramiko will throw an exception,
# so the SSH request must have succeeded.

print '--- Success! connecting to: ', ip_address
print '---               Username: ', username
print '---               Password: ', password
print '------------------------------------------------------\n'
