import os
cmd = 'systemctl status routechanger | grep "Active: active (running)"'
serviceRun = list(os.popen(cmd))
if serviceRun:
    print("running")
else:
    print("stope")
