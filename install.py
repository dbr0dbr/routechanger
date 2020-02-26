import os
import time
path = os.getcwd()
serviceName = 'routechanger'
serviceFile = '/etc/systemd/system/{name}.service'.format(name=serviceName)
if os.path.exists(serviceFile):
    try:
        print('stop {name}.service'.format(name=serviceName))
        os.popen('systemctl stop {name}'.format(name=serviceName))
        print("rm ", serviceFile)
        os.popen("rm {}".format(serviceFile))
    except: pass

time.sleep(1)

fileText = '''[Unit]
Description=Internet auto failover
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/env python3 {dir}/{name}.py

RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target 
'''
file = open(serviceFile, "w")
file.write(fileText.format(dir=path, name=serviceName))
file.close()
time.sleep(1)
try:
    os.popen('systemctl daemon-reload')
    time.sleep(1)
    os.popen('systemctl enable {name}'.format(name=serviceName))
    os.popen('systemctl start {name}'.format(name=serviceName))
    os.popen('systemctl status {name}'.format(name=serviceName))
except: pass