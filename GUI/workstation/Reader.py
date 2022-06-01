import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from threading import Thread
import time

# Access object for SimpleMFRC522


class Reader:
    GPIO.setwarnings(False)
    result = ""
    rfid = ""
    
    def __init__(self):
        self.result = "empty"
        self.rfid = SimpleMFRC522()

    def get_result(self):
        return self.result
    
    def reset_result(self):
        self.result = ""

    def reader(self):
        try:
            print("Place tag..")
            self.result = self.rfid.read()[1][:7]
            print("Data: " + str(self.result))
            time.sleep(1)

        # finally wird benoetigt, da die GPIO Pins ansonsten belegt bleiben
        finally:
            GPIO.cleanup()
