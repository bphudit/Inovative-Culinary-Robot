import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

#Energize solenoid valve with relay
def valveOn():
    GPIO.output(18, 1)

#De-energize solenoid valve with relay
def valveOff():
    GPIO.output(18, 0)










