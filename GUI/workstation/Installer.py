import os
import time


class Installer:
    def setup_network(self, address):
        os.system("sudo systemctl stop dhcpcd")
        os.system("sudo systemctl disable dhcpcd")
        write_netconfig = open("/etc/network/interfaces.d/eth0", "w")
        write_netconfig.write("auto eth0\n")
        write_netconfig.write("allow-hotplug eth0\n")
        write_netconfig.write("address " + address + "\n")
        write_netconfig.write("netmask 255.255.0.0")
        write_netconfig.write("gateway 169.254.0.1")
        write_netconfig.write("dns-nameservers 169.254.0.1")
        write_netconfig.write("dns-search domain-name")
        write_netconfig.close()
        os.system("sudo systemctl restart networking")
        os.system("cat /etc/resolv.conf")
        os.system("reboot")


    def install(self):
        try:
            print("Set SPI to on \n chose [5 – Interfacing Options]  [P4 – SPI]  [YES]  [OK]  [Finish]")
            time.sleep(3)
            os.system("sudo raspi-config")
            os.system("lsmod | grep spi")

            print("Installing os dependency's...")
            os.system("sudo apt-get update")
            os.system("sudo apt-get upgrade -y")

            print("Installing library's....")
            os.system("sudo apt-get -y install libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libopenjp2-7 libtiff5")

            print("Creating Fileserver link ...")
            os.system("mkdir /home/pi/Desktop/Fileserver")
            os.system("sudo mount -t cifs -o username=pi,password=raspberry "
                      "//169.254.0.2/WorkflowInstructions /home/pi/Desktop/Fileserver")
            os.system("sudo chmod -R 777 /home/pi/Desktop/Fileserver")
        except:
            print("Check the base installation commands.")

        try:
            import RPi.GPIO as GPIO
            from mfrc522 import SimpleMFRC522
            os.system("ls /usr/local/lib/python3.9/dist-packages/mfrc522 | grep MFRC522")
            time.sleep(2)
        except ImportError:
            print("Installing RFID packages...")
            os.system("sudo apt-get -y install python3-dev python3-pip")
            os.system("sudo pip3 install spidev")
            os.system("sudo pip3 install mfrc522")
            os.system("ls /usr/local/lib/python3.9/dist-packages/mfrc522 | grep MFRC522")
            time.sleep(2)
            import RPi.GPIO as GPIO
            from mfrc522 import SimpleMFRC522

        try:
            from threading import Thread
            import socket
        except ImportError:
            print("Baseimports are not working.")

        try:
            import _tkinter
            import tkinter
            from PIL import Image, ImageTk
        except ImportError:
            print("Installing tkinter packages...")
            os.system("sudo apt-get install python3-pil python3-pil.imagetk")
            import _tkinter
            import tkinter
            from PIL import Image, ImageTk

        try:
            from modules import Client
            from modules.Writer import Writer
            from modules.Reader import Reader
        except:
            print("module loading failed, check modules directory.")

        print("Rebooting the system in 3s...")
        time.sleep(3)
        os.system("sudo reboot")

if __name__ == "__main__":
    Installer().install()
