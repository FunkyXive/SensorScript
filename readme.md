# SensorScript
**Setup**
To setup SensorScript on a Raspberry PI you need to do a couple of things on your Raspberry PI first. The Setup Guide is based on a Raspberry PI Zero W with the lightest Raspbian installation.

**Setting up Raspberry PI**
You need to do a couple of things to configure the Raspberry PI

 1. Open config:`sudo raspi-config`
 2. Open network options and click on hostname. Set hostname to room and building number. For example 'mu7-5'.
 3. Open wifi and enter ssid and password for SKPWIFI.
 4. Go to main menu of config and click on boot options > desktop/cli > console autologin. 
 5. Go back to main menu of config and click on localization options and enter correct timezone.
 6. Go to interfacing options > ssh and enable ssh.
 7. Setup is finished.

**Running SetupScript.py**
To prepare the Raspberry PI for running as a temperature sensor you need to run SetupScript.py. The setup script determines which sensor script needs to run on the Raspberry PI. It also installs the needed python modules. To run the setup script you need to:

 1. Navigate to /home/pi: `cd /home/pi`
 2. Clone SetupScript.py to the Raspberry PI: `sudo wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SetupScript.py`
 3. Run SetupScript.py: `python3 pathto/SetupScript.py`
 4. When it prompts you for amount of sensors, enter the amount of sensors connected to the Raspberry PI. At the moment the limit is 2 sensors.
 5. Your Raspberry PI is now ready to be used as a temperature sensor.

**Rewriting sensor scripts for different uses**
You are welcome to change the sensor scripts to fit your needs. The code is commented to ease the revision of sensor scripts