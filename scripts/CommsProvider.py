import os
import json
import datetime
import time
import subprocess

ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

p = subprocess.Popen(['netstat','-i'],stdout=subprocess.PIPE)
out,err = p.communicate()
p = subprocess.Popen(['grep','wlan0'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
out,err = p.communicate(out)
p = subprocess.Popen(['sed','-r','s/wlan0[\\t ]+1500[\\t ]+([0-9]+).+/\\1/'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
rx,err = p.communicate(out)
p = subprocess.Popen(['sed','-r','s/wlan0[\\t ]+1500[\\t ]+[0-9]+[\\t ]+[0-9]+[\\t ]+[0-9]+[\\t ]+[0-9]+[\\t ]+([0-9]+).+/\\1/'],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
tx,err = p.communicate(out)

rx = int(rx.decode('utf-8'))
tx = int(tx.decode('utf-8'))

rx_json_string = '{"id": "comms.recd","timestamp": "'+ts+'","value":'+str(rx)+'}'
tx_json_string = '{"id": "comms.sent","timestamp": "'+ts+'","value":'+str(tx)+'}'

print(rx_json_string)
print(tx_json_string)
