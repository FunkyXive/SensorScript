#!/usr/bin/python
import datetime #import for timestamps in data
import requests #import for posting to the api
import time #import for keeping data checks regular
import os #import for making system commands
import socket #import for getting hostname and ip

imported = False #this while loo
while not imported:
    try:
        import Adafruit_DHT as DHT
    except ModuleNotFoundError as err:
        print(err)
    else:
        imported = True

ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
    [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
     [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]

hostname = socket.gethostname()
hostname = hostname.split("-")
name = hostname[0]
zone = int(hostname[1])
url = "http://infotavle.itd-skp.sde.dk/TH_API/ClimateSensor_Api/api/climateSensor/create.php"
pin = 4
lastCheck = time.time()
initialCheck = True
sensor = DHT.DHT22
try:
    while True:
        if time.time() - lastCheck >= 300 or initialCheck == True:
            lastCheck = time.time()
            initialCheck = False
            h, t = DHT.read_retry(sensor, pin)
            print(f"Temperature: {t}*C, Humidity: {h}%")
            r = requests.post(url, json={"ipaddress": ip, "zone": zone, "name": name, "updated": str(datetime.datetime.now()),
                                         "temperature": t, "humidity": h})
            print(r.status_code)
except (KeyboardInterrupt, SystemExit):
    raise
except:
    os.system('sudo reboot')
