import os

if os.path.isfile("SensorScript.py"):  # checks if the setup script is running on an already setup pi with one sensor
    os.system(
        "wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScript.py")  # if yes, we get the newest version from github to stay up to date
elif os.path.isfile(
        "SensorScriptDualSensor"):  # checks if the setup script is running on an already setup pi with two sensors
    os.system(
        "wget .N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScriptDualSensor.py")  # if yes, we get the newest version from github to stay up to date
else:
    amountOfSensors = input(
        "Enter the amount of sensors on your raspberryPi")  # at this point, there is no recognised sensorscripts running on the PI so we ask how many sensors is running on the pi
    if amountOfSensors == "1":  # if one we get the program made for one
        with open("/etc/profile", "a+") as f:
            if "python3 /home/pi/SetupScript" not in f:
                f.write("python3 /home/pi/SetupScript")
            if "python3 /home/pi/SensorScript.py" not in f:
                f.write("python3 /home/pi/SensorScript")
        os.system("wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScript.py")
    elif amountOfSensors == "2":  # if 2 we get the one made for 2
        with open("/etc/profile", "a+") as f:
            if "python3 /home/pi/SetupScript" not in f:
                f.write("python3 /home/pi/SetupScript")
            if "python3 /home/pi/SensorScript.py" not in f:
                f.write("python3 /home/pi/SensorScriptDualSensor")
        os.system("wget .N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScriptDualSensor.py")
    else:
        print(
            "sorry, that amount of sensors is not yet supported in the current scripts, look in the other scripts for inspiration for your own script")
