# /usr/bin/python
import datetime  # datetime import for time stamps in the http post request
import requests  # request import for the http post request to our webserver via the Api
import time  # time import for the regulation of data checks from the sensors
import socket  # socket import for the getting of ip and hostname
import os  # imports the os module so we can make system commands

imported = False
while not imported:  # while loop for importing of the Adafruit_DHT module
    try:  # this is in a try-except because the Adafruit_DHT module sometimes fails to import and crashes the program
        import Adafruit_DHT as DHT  # imports the Adafruit_DHT module with the alias DHT
    except ModuleNotFoundError as err:  # catches the error
        print(err)  # prints the error
    else:
        imported = True  # if the import is successful we continue

url = "http://infotavle.itd-skp.sde.dk/TH_API/ClimateSensor_Api/api/climateSensor/create.php"  # the url for our webserver

ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
    [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
     [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][
    0]  # this is for getting our ip, it is complicated because simply using socket.gethostbyname() often just returns 172.0.0.1
hostname = socket.gethostname()  # gets the host name of the device the script is running on
hostname = hostname.split("-")  # splits the hostname at "-" and converts it to a list
name = hostname[0]  # takes the first entry from the list and stores it as name
zoneFront = int(hostname[1])  # stores the second entry in the list as an int
zoneBack = int(hostname[2])  # stores the third entry in the list as an int
pinfront = 3  # the gpio pin that our front sensor's data pin is connected to
pinback = 4  # the gpio pin that our back sensor's data pin is connected to
lastCheck = time.time()  # sets the initial time for the lastCheck variable, used to only get data and post every 5 minutes
initialCheck = True  # sets initialCheck to true so we get data and post immediately once upon starting the script
sensor = DHT.DHT22  # defines which of the supported sensors of the module we are using
try:
    while True:  # the main running loop
        if time.time() - lastCheck >= 300 or initialCheck:  # checks if 5 minutes has passed since last check or if this is the first check after starting the script
            initialCheck = False  # sets initial check to false so we only run the loop every 5 minutes
            lastCheck = time.time()  # updates lastCheck to the new time of the last check
            fh, ft = DHT.read_retry(sensor,
                                    pinfront)  # gets humidity and heat from the front sensor, retries up to 15 times before returning none
            bh, bt = DHT.read_retry(sensor,
                                    pinback)  # gets the humidity and heat from the back sensor, retries up to 15 times before returning none
            print(
                f"Front temperature: {ft}*C, Front humidity: {fh}%, time sent: {datetime.datetime.now()}")  # prints the data from the front sensor in our cmdline
            print(
                f"Back temperature: {bt}*C, Front humidity: {bh}%, time sent: {datetime.datetime.now()}")  # prints the data fromt the back sensor in our cmdline
            fr = requests.post(url, json={"zone": zoneFront,
                                          "name": "ServerRoomFront",
                                          "ipaddress": ip,
                                          "updated": str(datetime.datetime.now()),
                                          "temperature": ft,
                                          "humidity": fh})  # posts the data from our front sensor as a json object to our server via the api
            br = requests.post(url, json={"zone": zoneBack,
                                          "name": "ServerRoomBack",
                                          "ipaddress": ip,
                                          "updated": str(datetime.datetime.now()),
                                          "temperature": bt,
                                          "humidity": bh})  # posts the data from our back sensor as a json object to our server via the api
            print("fr: ", fr.status_code, ", br: ",
            print(f"zone: {zoneFront}, Name: {'ServerRoomFront'}, ipaddress: {ip}, updated: {str(datetime.datetime.now())}, h: {fh}, t: {ft}")
            print(f"zone: {zoneBack}, Name: {'ServerRoomBack'}, ipaddress: {ip}, updated: {str(datetime.datetime.now())}, h: {bh}, t: {fh}")

except (KeyboardInterrupt, SystemExit):
    raise
except:
    os.system("sudo reboot")
