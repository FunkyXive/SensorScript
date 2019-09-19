import os

if os.path.isfile("SensorScript.py"):
    os.system("wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScript.py")
elif os.path.isfile("SensorScriptDualSensor"):
    os.system("wget .N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScriptDualSensor.py")
else:
    amountOfSensors = input("Enter the amount of sensors on your raspberryPi")
    if amountOfSensors == "1":
        os.system("wget -N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScript.py")
    elif amountOfSensors == "2":
        os.system("wget .N https://raw.githubusercontent.com/FunkyXive/SensorScript/master/SensorScriptDualSensor.py")
    else:
        print("sorry, that amount of sensors is not yet supported in the current scripts, look in the other scripts for inspiration for your own script")
