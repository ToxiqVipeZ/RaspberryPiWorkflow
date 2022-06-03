import os
import socket
import time
import sys


class Installer:
    def __init__(self):
        if sys.argv[1] == "setup_network":
            self.Setup_Network(sys.argv[2])
        elif sys.argv[1] == "setup_workstation":
            self.Setup_Workstation()

    def test_connection(self):
        try:
            socket.create_connection(("Google.de", 80))
            return True
        except OSError:
            return False

    def Setup_Network(self, address):
        os.system("sudo systemctl stop dhcpcd")
        os.system("sudo systemctl disable dhcpcd")
        write_netconfig = open("/etc/network/interfaces.d/eth0", "w")
        write_netconfig.write("auto eth0\n")
        write_netconfig.write("allow-hotplug eth0\n")
        write_netconfig.write("iface eth0 inet static\n")
        write_netconfig.write("address " + address + "\n")
        write_netconfig.write("netmask 255.255.0.0\n")
        write_netconfig.write("gateway 169.254.0.1\n")
        write_netconfig.write("dns-nameservers 169.254.0.1\n")
        write_netconfig.write("dns-search domain-name\n")
        write_netconfig.close()
        os.system("sudo systemctl restart networking")
        os.system("cat /etc/resolv.conf")

        print("\n################################\n"
              "Press \"Y\" to reboot. It's necessary.\n"
              "################################\n")
        confirmation = input()
        if confirmation != "Y":
            while confirmation != "Y":
                print("\n################################\n"
                      "Press \"Y\" to reboot. It's necessary.\n"
                      "################################\n")
                confirmation = input()
        if confirmation == "Y":
            print("\n################################\n"
                  "rebooting the system in 3s...\n"
                  "################################\n")
            time.sleep(3)
            os.system("sudo reboot")

    def Setup_Workstation(self):
        while not self.test_connection():
            print("sleeping for 3s .. retrying internet connection ..")
            time.sleep(3)

        try:
            print("\n################################\n"
                  "Setting raspi-config options...\n"
                  "################################\n")
            time.sleep(2)
            os.system("sudo raspi-config nonint do_spi 0")
            os.system("sudo raspi-config nonint do_vnc 0")
            os.system("sudo raspi-config nonint do_ssh 0")
            os.system("lsmod | grep spi")
            print("\n")

            print("\n################################\n"
                  "Installing os dependency's...\n"
                  "################################\n")
            time.sleep(2)
            os.system("sudo apt-get update")
            os.system("sudo apt-get upgrade -y")

            print("\n################################\n"
                  "Installing library's....\n"
                  "################################\n")
            time.sleep(2)
            os.system("sudo apt-get -y install libjpeg-dev zlib1g-dev libfreetype6-dev libopenjp2-7 libtiff5")

            print("\n################################\n"
                  "Creating Fileserver links ...\n"
                  "################################\n")
            time.sleep(2)
            os.system("mkdir /home/pi/Fileserver")
            os.system("sudo mount -t cifs -o username=pi,password=raspberry "
                      "//169.254.0.2/WorkflowInstructions /home/pi/Fileserver")
            os.system("sudo chmod -R 755 /home/pi/Fileserver")

            print("\n################################\n"
                  "Fetching the WorkstationApp from the Fileserver\n"
                  "################################\n")
            os.system("mkdir /home/pi/WorkstationApp")
            os.system("sudo mount -t cifs -o username=pi,password=raspberry "
                      "//169.254.0.2/WorkflowInstructions/WorkstationApp /home/pi/WorkstationApp")
            os.system("sudo chmod -R 755 /home/pi/WorkstationApp")

            automount_fstab = open("/etc/fstab", "a")
            automount_fstab.write("//169.254.0.2/WorkflowInstructions /home/pi/Fileserver cifs "
                                  "username=pi,password=raspberry 0 0\n")
            automount_fstab.write("//169.254.0.2/WorkflowInstructions/WorkstationApp /home/pi/WorkstationApp cifs "
                                  "username=pi,password=raspberry 0 0\n")
            automount_fstab.close()

        except:
            print("\n################################\n"
                  "Check the base installation commands.\n"
                  "################################\n")

        try:
            import RPi.GPIO as GPIO
            from mfrc522 import SimpleMFRC522
            os.system("ls /usr/local/lib/python3.9/dist-packages/mfrc522 | grep MFRC522")
            time.sleep(2)
        except ImportError:
            print("\n################################\n"
                  "Installing RFID packages...\n"
                  "################################\n")
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
            print("\n################################\n"
                  "Baseimports are not working.\n"
                  "################################\n")

        try:
            import _tkinter
            import tkinter
            from PIL import Image, ImageTk
        except ImportError:
            print("\n################################\n"
                  "Installing tkinter packages...\n"
                  "################################\n")
            os.system("sudo apt-get -y install python3-pil python3-pil.imagetk")
            import _tkinter
            import tkinter
            from PIL import Image, ImageTk

        try:
            os.system("cd /home/pi/WorkflowApp")
            from modules import Client
            from modules.Writer import Writer
            from modules.Reader import Reader
        except:
            print("\n################################\n"
                  "module loading failed, check modules directory.\n"
                  "################################\n")

        try:
            print("\n################################\n"
                  "Setup of autonomic WorkstationApp start at launch...\n"
                  "################################\n")
            time.sleep(2)

            os.system("cd /home/pi/Desktop")
            os.system("echo \"#!/bin/bash\nsleep 10\ncd /home/pi/WorkstationApp\npython3 WorkstationApp.py\ncd /\""
                      " > WorkstationLauncher.sh")

            autostart_workstation_app = open("/etc/xdg/lxsession/LXDE-pi/autostart", "a")
            autostart_workstation_app.write("@lxterminal -e bash /home/pi/Desktop/WorkstationLauncher.sh")
            autostart_workstation_app.close()
        except:
            print("\n################################\n"
                  "Setup of autonomic WorkstationApp start at launch failed.\n"
                  "################################\n")

        print("\n################################\n"
              "Press \"Y\" to reboot. It's necessary.\n"
              "################################\n")
        confirmation = input()

        if confirmation != "Y":
            print("\n################################\n"
                  "Press \"Y\" to reboot. It's necessary.\n"
                  "################################\n")
            confirmation = input()

        elif confirmation == "Y":
            print("\n################################\n"
                  "Rebooting the system in 5s...\n"
                  "################################\n")
            time.sleep(5)
            os.system("sudo reboot")

if __name__ == "__main__":
    Installer()
