import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time


# Objekt mit Zugriff auf Methoden von SimpleMFRC522
rfid = SimpleMFRC522()
GPIO.setwarnings(False)
newRFID = ""

class Writer:
    def __init__(self, value):
        self.newRFID = str(value)
        self.main()

    def main(self):
        try:
            input_text = self.newRFID
            print("Place tag..")

            rfid.write(input_text)
            print("written. sleep 5 sec...")

            time.sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()

        # finally wird benötigt, da die GPIO Pins ansonsten belegt bleiben
        finally:
            GPIO.cleanup()

