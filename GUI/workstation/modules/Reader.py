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
    
try:
    from threading import Thread
except ImportError:
    print("Thread import failed.")

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
