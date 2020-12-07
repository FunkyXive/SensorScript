#!/usr/bin/python
import datetime  # import for timestamps in data
import requests  # import for posting to the api
import time  # import for keeping data checks regular
import os  # import for making system commands
import socket  # import for getting hostname and ip

imported = False
while not imported:  # The Adafruit_DHT module is sometimes not getting imported and will then crash the program, this is to ensure that we import it
    try:
        import Adafruit_DHT as DHT
    except ModuleNotFoundError as err:
        print(err)
    else:
        imported = True

ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [
    [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
     [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][
    0]  # this piece of code gets the ip address that is used to access the internet

hostname = socket.gethostname()  # gets the host name of the device the script is running on
hostname = hostname.split("-")  # splits the hostname at "-" and converts it to a list
name = hostname[0]  # takes the first entry from the list and stores it as name, this is usually the building identifier
zone = int(hostname[1])  # stores the second entry in the list as an int, this is usually the zone identifier
# the above two variables then gives us a way to identify each sensor, fx: mu1a-7 would be building 1a zone 7
url = "http://infotavle.itd-skp.sde.dk/TH_API/ClimateSensor_Api/api/climateSensor/create.php"  # urlL of our api
pin = 4  # the io pin on our raspberry pi that is connected to the data pin on the DHT22
lastCheck = time.time()  # set's the initial last check time
sensorStartHour = 6  # the hour to start sensors
sensorEndHour = 18  # the end hour for the sensors
initialCheck = True  # sets initial-check to true so we get first reading immediately
sensor = DHT.DHT22  # defines which sensor of the supported sensors that we are using
temperatureDeviance = 0.5  # variable controlling how much the temperature needs to change each check
last_hum, last_temp = 1, 1  # random base value for last check that makes the sensor always send when started up


def save_to_log(post_status_code, message, error_log=False):  # function to write to local log file
    if error_log:  # checks if error_log is true, if so we write to a seperate file from regular log
        with open('error_log.txt',
                  'a+') as f:  # opens our log file, creating it if it doesn't exist , using with open to automatically close the file when we're done using it
            f.write(
                f"{datetime.datetime.now()} posted:{message}, status code: {post_status_code}\n")  # we write to the file the current time, then the message and the statuscode of a post
            if len(open('error_log.txt').readlines()) >= 10:  # check if log file is longer than a certain amount,
                print("error_log file longer than 10 lines, deleting first line")  # prints that the file is longer
                os.system(
                    r'echo "$(tail -n +2 error_log.txt)" > error_log.txt')  # deletest the first line of the file aka the oldest to reduce file size and maintenece
    else:  # if error_log is false do the regular logging
        with open('log.txt',
                  'a+') as f:  # opens our log file, creating it if it doesn't exist , using with open to automatically close the file when we're done using it
            f.write(
                f"{datetime.datetime.now()} posted:{message}, status code: {post_status_code}\n")  # we write to the file the current time, then the message and the statuscode of a post
            if len(open('log.txt').readlines()) >= 10:  # check if log file is longer than a certain amount,
                print("file longer than 10 lines, deleting first line")  # prints that the file is longer
                os.system(
                    r'echo "$(tail -n +2 log.txt)" > log.txt')  # deletest the first line of the file aka the oldest to reduce file size and maintenece


def static_check(current_time, check_hour, check_minute):  # function for preset static checks at the same time every day
    if current_time.hour == check_hour and current_time.minute == check_minute:  # checks if we are at the entered hour and minute
        h, t = DHT.read_retry(sensor,
                              pin)  # reads humidity and temperature from sensor, retries up to 15 times if it fails
        print(f"Temperature: {t}*C, Humidity: {h}%")  # prints the data for testing and monitoring purposes
        r = requests.post(url, json={"ipaddress": ip,
                                     "zone": zone,
                                     "name": name,
                                     "updated": str(datetime.datetime.now()),
                                     "temperature": t,
                                     "humidity": h})  # posting the data as json to our api via the url
        print(r.status_code)  # prints the status code of the post request 201 for success
        save_to_log(r.status_code, t)  # save to log
        print(f"posted static {check_hour}")  # prints to the pi that this specific post was static and the current hour
        last_hum, last_temp = h, t  # sets the last check temp and hum
        if r.status_code == 201:  # checks if the post request was succesful
            time.sleep(
                300)  # if yes, sleeps for 1 minute and 1 second as to not post the same data twice in one static check call


try:  # try except so we restart the raspberry pi if the program crashes
    while True:  # main data loop
        current_time = datetime.datetime.now()  # gets the current time
        hour = current_time.hour  # gets the current hour 0-23
        static_check(current_time, 8, 0)  # static check at hour 8 minute 0 aka 8 am
        static_check(current_time, 12, 0)
        static_check(current_time, 15, 0)
        if sensorStartHour <= hour <= sensorEndHour:  # checks if current hour is between start hour and end hour, if true, run hour script, if not don't
            if time.time() - lastCheck >= 60 or initialCheck:  # checks if 1(60seconds) minutes has passed since last check or if this is the first check since we started the program
                lastCheck = time.time()  # updates the lastCheck variable to the new time
                h, t = DHT.read_retry(sensor,
                                      pin)  # reads humidity and temperature from sensor, retries up to 15 times if it fails
                if abs(
                        t - last_temp) >= temperatureDeviance or initialCheck:  # checks if the difference between the current temp and last temp is more than the set deviance threshold, if it is then it sends data, if not it prints the temp difference
                    initialCheck = False  # sets initialCheck to false so we don't spam the server
                    print(f"Temperature: {t}*C, Humidity: {h}%")  # prints the data for testing and monitoring purposes
                    r = requests.post(url, json={"ipaddress": ip,
                                                 "zone": zone,
                                                 "name": name,
                                                 "updated": str(datetime.datetime.now()),
                                                 "temperature": t,
                                                 "humidity": h})  # posting the data as json to our api via the url
                    print(r.status_code)  # prints the status code of the post request 201 for success
                    save_to_log(r.status_code, t)  # saves to log
                    last_hum, last_temp = h, t  # sets the last check temp and hum
                    print("posted")
                else:
                    print(abs(t - last_temp), f"temp, last_temp: {t}, {last_temp}")  # prints the deviance
        else:
            print(f"not posting{sensorStartHour}{hour}{sensorEndHour}")
            initialCheck = True  # sets initial check to true so we post data on first check in the specified time frame
            time.sleep(10)

except (KeyboardInterrupt, SystemExit) as e:  # makes it so the pi doesn't restart at the exceptions specified
    save_to_log("nothing was posted", "Exception: KeyboardInterrupt", error_log=True)
    raise
except Exception as e:  # restarts the raspberry pi on all other exceptions and saves the exception in e
    r = requests.post(url, json={"Error": str(e), "zone": zone, "name": name,
                                 "errorTime": str(datetime.datetime.now())})  # posts error information to our server
    print(r.status_code)  # prints the status code of the above request
    save_to_log(r.status_code, e, error_log=True)  # saves to log
    print("posted")  # prints "posted"
    print(e)  # prints the exception to our console for debugging purposes
    time.sleep(5)
    os.system('sudo reboot')  # reboot system command
