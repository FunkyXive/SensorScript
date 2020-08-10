import os
import time
if os.path.isfile("SensorScript.py"):  # checks if the setup script is running on an already setup pi with one sensor
    os.system(
        "sudo wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScript.py")  # if yes, we get the newest version from github to stay up to date
elif os.path.isfile(
        "SensorScriptDualSensor.py"):  # checks if the setup script is running on an already setup pi with two sensors
    os.system(
        "sudo wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScriptDualSensor.py")  # if yes, we get the newest version from github to stay up to date
else:
    amountOfSensors = input(
        "Enter the amount of sensors on your raspberryPi")  # at this point, there is no recognised sensorscripts running on the PI so we ask how many sensors is running on the pi
    building = input("Enter the number of the building the sensor will be in")
    zone = input("Enter the zone number the sensor will be in")
    if amountOfSensors == "1":  # if one we get the program made for one
        os.system("sudo apt install python3-pip") #installs the pip package manager for python3
        os.system("sudo pip3 install Adafruit_DHT") #installs the library for using the dht22 sensor using pip

        with open("/etc/hostname", "w") as f:
            f.writelines(f"mu{building}-{zone}")
        with open("/etc/network/interfaces", "a+") as f:
            f.writelines("auto wlan0")
            f.writelines("iface wlan0 inet dhcp")
            f.writelines("                wpa-ssid SKPWIFI")
            f.writelines("                wpa-psk  SKPWire1!")
        os.system("sudo dhclient wlan0")

        with open("etc/systemd/system/getty@tty1.service.d/autologin.conf") as f:
            f.writelines("[service]")
            f.writelines("ExecStart=")
            f.writelines("ExecStart=-/sbin/agetty --autologin pi --noclear %I $TERM")

        os.system("sudo timedatectl set-timezone Europe/Copenhagen")
        with open("/etc/profile") as f: #opens the file /etc/profile, this file does multiple things, we just need it to add files run on startup
            if "python3 /home/pi/SetupScript.py" not in f:  #checks if the setupscript is alreadu in the file
                with open("/etc/profile", "a+") as f1: #opens the file at the end of the file
                    f1.writelines("python3 /home/pi/SetupScript.py \n") #if the SetupScript isn't in the file, it adds the SetupScript to the startup running scripts
        with open("/etc/profile") as f: #the same for the sensor script, we add both so it automatically get's the newest version from github when the pi starts up
            if "python3 /home/pi/SensorScript.py" not in f:
                with open("/etc/profile", "a+") as f1:
                    f1.writelines("python3 /home/pi/SensorScript.py \n")
        os.system("wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScript.py") #get's the sensorscript from github and saves it in the location this script is run
        print("wait........")
        time.sleep(2)
        print(".")
        time.sleep(2)
        print("..")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("Setup Complete!")
        time.sleep(2)
        print("Restarting...")
        time.sleep(2)
        os.system("sudo reboot")
    elif amountOfSensors == "2":  # if 2 we get the one made for 2
        os.system("sudo apt install python3-pip")
        os.system("sudo pip3 install Adafruit_DHT")
        with open("/etc/profile", "a+") as f:
            if "python3 /home/pi/SetupScript.py" not in f:
                f.writelines("python3 /home/pi/SetupScript.py")
            if "python3 /home/pi/SensorScript.py" not in f:
                f.writelines("python3 /home/pi/SensorScriptDualSensor.py")
        os.system("wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScriptDualSensor.py")
        print("wait........")
        time.sleep(2)
        print(".")
        time.sleep(2)
        print("..")
        time.sleep(2)
        print("...")
        time.sleep(2)
        print("Setup Complete!")
        time.sleep(2)
        print("Restarting...")
        time.sleep(2)
        os.system("sudo reboot")
    else:
        print(
            "sorry, that amount of sensors is not yet supported in the current scripts, look in the other scripts for inspiration for your own script.")


