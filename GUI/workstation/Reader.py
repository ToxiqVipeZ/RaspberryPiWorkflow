import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import os

# Objekt mit Zugriff auf Methoden von SimpleMFRC522
rfid = SimpleMFRC522()
#wsa = WorkstationApp.WorkstationApp()
GPIO.setwarnings(False)


class Reader:
    def __init__(self):
        """
        Initialisation method
        :param rfid_init: saves the RFID on object creation or class call in rfid_scanned
        """
        #self.rfid_scanned = rfid_init
        self.main()

    def main(self):
        try:
            print("Place tag..")
            result = rfid.read()
            print("Data: " + str(result[1]))
            print("Sleeping 3s!")
            time.sleep(1)
            #print(str(result[1]))
            return str(result[1])

        except KeyboardInterrupt:
            GPIO.cleanup()

        # finally wird benoetigt, da die GPIO Pins ansonsten belegt bleiben
        finally:
            GPIO.cleanup()

