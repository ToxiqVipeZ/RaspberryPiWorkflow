import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time


# Objekt mit Zugriff auf Methoden von SimpleMFRC522


class Writer:
    GPIO.setwarnings(False)
    newRFID = ""
    rfid = ""
    
    def __init__(self, value):
        self.newRFID = str(value)
        self.main()

    def main(self):
        try:
            input_text = self.newRFID
            print("Place tag..")

            rfid.write(input_text)
            print("written.")
            
            print(rfid.read()[1]+"x")
            time.sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()

        # finally wird benötigt, da die GPIO Pins ansonsten belegt bleiben
        finally:
            GPIO.cleanup()
