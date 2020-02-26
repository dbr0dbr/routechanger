from provider import Provider
first = Provider(name ='WNet', 
                gatway = '192.168.30.10', 
                test_hosts = ['8.26.56.8', '37.235.1.174'])
second = Provider(name = 'DTS',
                 gatway =  "192.168.30.254", 
                 test_hosts = ['8.20.247.20', '37.235.1.177'])
log = "/var/log/routechanger.log"
