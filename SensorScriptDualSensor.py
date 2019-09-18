# /usr/bin/python
import datetime
import requests
import time
import socket

imported = False
while not imported:
    try:
        import Adafruit_DHT as DHT
    except ModuleNotFoundError as err:
        print(err)
    else:
        imported = True

url = "http://infotavle.itd-skp.sde.dk/TH_API/ClimateSensor_Api/api/climateSensor/create.php"

ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
    [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
     [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][
    0]
hostname = socket.gethostname()  # gets the host name of the device the script is running on
hostname = hostname.split("-")  # splits the hostname at "-" and converts it to a list
name = hostname[0]  # takes the first entry from the list and stores it as name
zoneFront = int(hostname[1])  # stores the second entry in the list as an int
zoneBack = int(hostname[2])  # stores the third entry in the list as an int
pinfront = 3
pinback = 4
lastCheck = time.time()
initialCheck = True
sensor = DHT.DHT22
while True:
    if time.time() - lastCheck >= 300 or initialCheck == True:
        initialCheck = False
        lastCheck = time.time()
        fh, ft = DHT.read_retry(sensor, pinfront)
        bh, bt = DHT.read_retry(sensor, pinback)
        print(f"Front temperature: {ft}*C, Front humidity: {fh}%, time sent: {datetime.datetime.now()}")
        print(f"Back temperature: {bt}*C, Front humidity: {bh}%, time sent: {datetime.datetime.now()}")
        fr = requests.post(url, json={"zone": 100,
                                      "name": "ServerRoomFront",
                                      "updated": str(datetime.datetime.now()),
                                      "temperature": ft,
                                      "humidity": fh})
        br = requests.post(url, json={"zone": 102,
                                      "name": "ServerRoomBack",
                                      "updated": str(datetime.datetime.now()),
                                      "temperature": bt,
                                      "humidity": bh})
        print("fr: ", fr.status_code, ", br: ", br.status_code)
