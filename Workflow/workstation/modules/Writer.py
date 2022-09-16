try:
    import RPi.GPIO as GPIO
except ImportError:
    print("GPIO import failed.")
    
try:
    from mfrc522 import SimpleMFRC522
except ImportError:
    print("SimpleMFRC522 import failed.")
    
try:
    import time
except ImportError:
    print("time import failed.")

# Objekt mit Zugriff auf Methoden von SimpleMFRC522


class Writer:
    GPIO.setwarnings(False)
    newRFID = ""
    rfid = ""
    
    def __init__(self, value):
        self.newRFID = str(value)
        self.rfid = SimpleMFRC522()
        self.main()

    def main(self):
        try:
            input_text = self.newRFID
            print("(Writer) Place tag: ")

            self.rfid.write(input_text)
            print("Written: " + self.rfid.read()[1][:7])

            time.sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()

        # finally wird benötigt, da die GPIO Pins ansonsten belegt bleiben
        finally:
            GPIO.cleanup()
