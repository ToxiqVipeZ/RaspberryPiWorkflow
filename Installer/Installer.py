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
        elif sys.argv[1] == "setup_warehouse":
            self.Setup_Warehouse()
        elif sys.argv[1] == "setup_server":
            self.Setup_Server()

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

    def Setup_Server(self):
        while not self.test_connection():
            print("sleeping for 3s .. retrying internet connection ..")
            time.sleep(3)

        try:
            print("\n################################\n"
                  "Setting raspi-config options...\n"
                  "################################\n")
            time.sleep(2)
            os.system("sudo raspi-config nonint do_vnc 0")
            os.system("sudo raspi-config nonint do_ssh 0")
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
                  "Fetching the files from the Fileserver.\n"
                  "################################\n")
            os.system("mkdir /home/pi/ServerFiles")
            os.system("sudo mount -t cifs -o username=pi,password=raspberry "
                      "//169.254.0.2/ServerFiles /home/pi/ServerFiles")
            os.system("sudo chmod -R 755 /home/pi/ServerFiles")

            automount_fstab = open("/etc/fstab", "a")
            automount_fstab.write("//169.254.0.2/ServerFiles /home/pi/ServerFiles cifs "
                                  "username=pi,password=raspberry 0 0\n")
            automount_fstab.close()

        except:
            print("\n################################\n"
                  "Installer failed. Check the base installation commands.\n"
                  "################################\n")

        try:
            from threading import Thread
            import socket
        except ImportError:
            print("\n################################\n"
                  "Baseimports are not working.\n"
                  "################################\n")

        try:
            import mysql.connector

        except ImportError:
            print("\n################################\n"
                  "Installing mysql packages...\n"
                  "################################\n")
            os.system("pip3 install mysql.connector")
            import mysql.connector

        print("\n################################\n"
              "Setup of autonomic StorageApp start at launch...\n"
              "################################\n")

        try:
            time.sleep(2)
            "/bash\necho \"WorkstationApp wird in 5s gestartet...\"\nsleep 5\nc"
            # Server starter:
            os.system("cd /home/pi/ServerFiles/Server/")
            os.system(
                "echo \"#!/bin/bash\necho \"Server wird in 3s gestartet...\"\nsleep 3\ncd /home/pi/ServerFiles/Server"
                "\npython3 Server.py"
                "\ncd /\" > /home/pi/ServerFiles/Server/ServerLauncher.sh")
            os.system("sudo chmod 755 /home/pi/ServerFiles/Server/ServerLauncher.sh")
            # DBQueue starter:
            os.system("cd /home/pi/ServerFiles/Server/Standalones")
            os.system(
                "echo \"#!/bin/bash\necho \"DBQueue wird in 3s gestartet...\"\nsleep 3\ncd /home/pi/ServerFiles/Server/"
                "Standalones\npython3 DatabaseQueue.py"
                "\ncd /\" > /home/pi/ServerFiles/Server/Standalones/DatabaseQueueLauncher.sh")
            os.system("sudo chmod 755 /home/pi/ServerFiles/Server/Standalones/DatabaseQueueLauncher.sh")
            # SIC starter:
            os.system("cd /home/pi/ServerFiles/Server/Standalones/")
            os.system(
                "echo \"#!/bin/bash\necho \"SIC wird in 3s gestartet...\"\nsleep 3\ncd /home/pi/ServerFiles/Server/"
                "Standalones\npython3 ShopInformationCollector.py"
                "\ncd /\" > /home/pi/ServerFiles/Server/Standalones/SICLauncher.sh")
            os.system("sudo chmod 755 /home/pi/ServerFiles/Server/Standalones/SICLauncher.sh")

            autostart_server_apps = open("/etc/xdg/lxsession/LXDE-pi/autostart", "a")
            autostart_server_apps.write(
                "@lxterminal -e bash /home/pi/ServerFiles/Server/ServerLauncher.sh"
                "@lxterminal -e bash /home/pi/ServerFiles/Server/Standalones/DatabaseQueueLauncher.sh"
                "@lxterminal -e bash /home/pi/ServerFiles/Server/Standalones/SICLauncher.sh"
            )
            autostart_server_apps.close()

            os.system("cd /home/pi/Desktop/")
            os.system("echo \"[Desktop Entry]\n"
                      "Type=Application\n"
                      "Name=ServerLauncher\n"
                      "Terminal=true\n"
                      "Exec=/home/pi/ServerFiles/Server/ServerLauncher.sh\n"
                      "Icon=/home/pi/ServerFiles/Logos/desktoplogo.png\n\" > /home/pi/Desktop/ServerLauncher.desktop")

            os.system("cd /home/pi/Desktop/")
            os.system("echo \"[Desktop Entry]\n"
                      "Type=Application\n"
                      "Name=DBQueueLauncher\n"
                      "Terminal=true\n"
                      "Exec=/home/pi/ServerFiles/Server/Standalones/DatabaseQueueLauncher.sh\n"
                      "Icon=/home/pi/ServerFiles/Logos/desktoplogo.png\n\" > /home/pi/Desktop/DBQueueLauncher.desktop")

            os.system("cd /home/pi/Desktop/")
            os.system("echo \"[Desktop Entry]\n"
                      "Type=Application\n"
                      "Name=SICLauncher\n"
                      "Terminal=true\n"
                      "Exec=/home/pi/ServerFiles/Server/Standalones/SICLauncher.sh\n"
                      "Icon=/home/pi/ServerFiles/Logos/desktoplogo.png\n\" > /home/pi/Desktop/SICLauncher.desktop")

            os.system("sudo rm /etc/xdg/lxsession/LXDE-pi/sshpwd.sh")

        except:
            print("\n################################\n"
                  "Setup of autonomic StorageManager start at launch failed.\n"
                  "################################\n")

        print("\n################################\n"
              "Press \"Y\" to reboot. It's necessary.\n"
              "################################\n")
        confirmation = input()

        if confirmation != "Y":
            print("\n################################\n"
                  "Enter \"Y\" to reboot. It's necessary.\n"
                  "################################\n")
            confirmation = input()

        elif confirmation == "Y":
            print("\n################################\n"
                  "Rebooting the system in 5s...\n"
                  "################################\n")
            time.sleep(5)
            os.system("sudo reboot")

    def Setup_Warehouse(self):
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
                  "Fetching the files from the Fileserver.\n"
                  "################################\n")
            os.system("mkdir /home/pi/ServerFiles")
            os.system("sudo mount -t cifs -o username=pi,password=raspberry "
                      "//169.254.0.2/ServerFiles /home/pi/ServerFiles")
            os.system("sudo chmod -R 755 /home/pi/ServerFiles")

            automount_fstab = open("/etc/fstab", "a")
            automount_fstab.write("//169.254.0.2/ServerFiles /home/pi/ServerFiles cifs "
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
            # moving the modfied RFID library to the library destination
            os.system(
                "sudo cp /home/pi/ServerFiles/Workflow/Workstation/modules/SimpleMFRC522.py "
                "/usr/local/lib/python3.9/dist-packages/mfrc522/")
            time.sleep(2)
        except ImportError:
            print("\n################################\n"
                  "Installing RFID packages...\n"
                  "################################\n")
            os.system("sudo apt-get -y install python3-dev python3-pip")
            os.system("sudo pip3 install spidev")
            os.system("sudo pip3 install mfrc522")
            os.system("ls /usr/local/lib/python3.9/dist-packages/mfrc522 | grep MFRC522")
            # moving the modfied RFID library to the library destination
            os.system(
                "sudo cp /home/pi/ServerFiles/Workflow/Workstation/modules/SimpleMFRC522.py "
                "/usr/local/lib/python3.9/dist-packages/mfrc522/")
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
            import ttkthemes
            from PIL import Image, ImageTk
        except ImportError:
            print("\n################################\n"
                  "Installing tkinter packages...\n"
                  "################################\n")
            os.system("sudo apt-get -y install python3-pil python3-pil.imagetk")
            os.system("python3 -m pip install git+https://github.com/RedFantom/ttkthemes")
            import _tkinter
            import tkinter
            import ttkthemes
            from PIL import Image, ImageTk

        try:
            import mysql.connector

        except ImportError:
            print("\n################################\n"
                  "Installing mysql packages...\n"
                  "################################\n")
            os.system("pip3 install mysql.connector")
            import mysql.connector

        try:
            print("\n################################\n"
                  "Setup of autonomic StorageApp start at launch...\n"
                  "################################\n")
            time.sleep(2)

            os.system("cd /home/pi/ServerFiles/StorageManagement/GUI/")
            os.system(
                "echo \"#!/bin/bash\nsleep 5\ncd /home/pi/ServerFiles/StorageManagement/GUI\npython3 StorageWorker.py"
                "\ncd /\" > /home/pi/ServerFiles/StorageManagement/GUI/StorageWorkerLauncher.sh")
            os.system("sudo chmod 755 /home/pi/ServerFiles/StorageManagement/GUI/StorageWorkerLauncher.sh")

            os.system("cd /home/pi/ServerFiles/StorageManagement/GUI/")
            os.system(
                "echo \"#!/bin/bash\nsleep 5\ncd /home/pi/ServerFiles/StorageManagement/GUI\npython3 StorageManager.py"
                "\ncd /\" > /home/pi/ServerFiles/StorageManagement/GUI/StorageManagerLauncher.sh")
            os.system("sudo chmod 755 /home/pi/ServerFiles/StorageManagement/GUI/StorageManagerLauncher.sh")

            autostart_workstation_app = open("/etc/xdg/lxsession/LXDE-pi/autostart", "a")
            autostart_workstation_app.write(
                "@lxterminal -e bash /home/pi/ServerFiles/StorageManagement/GUI/StorageWorkerLauncher.sh")
            autostart_workstation_app.close()

            os.system("cd /home/pi/Desktop/")
            os.system("echo \"[Desktop Entry]\n"
                      "Type=Application\n"
                      "Name=StorageWorker\n"
                      "Terminal=true\n"
                      "Exec=/home/pi/ServerFiles/StorageManagement/GUI/StorageWorkerLauncher.sh\n"
                      "Icon=/home/pi/ServerFiles/Logos/desktoplogo.png\n\" > /home/pi/Desktop/StorageWorker.desktop")

            os.system("cd /home/pi/Desktop/")
            os.system("echo \"[Desktop Entry]\n"
                      "Type=Application\n"
                      "Name=StorageManager\n"
                      "Terminal=true\n"
                      "Exec=/home/pi/ServerFiles/StorageManagement/GUI/StorageManagerLauncher.sh\n"
                      "Icon=/home/pi/ServerFiles/Logos/desktoplogo.png\n\" > /home/pi/Desktop/StorageManager.desktop")

            os.system("sudo rm /etc/xdg/lxsession/LXDE-pi/sshpwd.sh")

        except:
            print("\n################################\n"
                  "Setup of autonomic StorageManager start at launch failed.\n"
                  "################################\n")

        print("\n################################\n"
              "Press \"Y\" to reboot. It's necessary.\n"
              "################################\n")
        confirmation = input()

        if confirmation != "Y":
            print("\n################################\n"
                  "Enter \"Y\" to reboot. It's necessary.\n"
                  "################################\n")
            confirmation = input()

        elif confirmation == "Y":
            print("\n################################\n"
                  "Rebooting the system in 5s...\n"
                  "################################\n")
            time.sleep(5)
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
                  "Creating workflow instructions links ...\n"
                  "################################\n")
            time.sleep(2)
            os.system("mkdir /home/pi/WorkflowInstructions")
            os.system("sudo mount -t cifs -o username=pi,password=raspberry "
                      "//169.254.0.2/WorkflowInstructions /home/pi/WorkflowInstructions")
            os.system("sudo chmod -R 755 /home/pi/WorkflowInstructions")

            print("\n################################\n"
                  "Fetching the files from the Fileserver.\n"
                  "################################\n")
            os.system("mkdir /home/pi/ServerFiles")
            os.system("sudo mount -t cifs -o username=pi,password=raspberry "
                      "//169.254.0.2/ServerFiles /home/pi/ServerFiles")
            os.system("sudo chmod -R 755 /home/pi/ServerFiles")

            automount_fstab = open("/etc/fstab", "a")
            automount_fstab.write("//169.254.0.2/WorkflowInstructions /home/pi/WorkflowInstructions cifs "
                                  "username=pi,password=raspberry,uid=1000,gid=1000 0 0\n")
            automount_fstab.write("//169.254.0.2/ServerFiles /home/pi/ServerFiles cifs "
                                  "username=pi,password=raspberry,uid=1000,gid=1000 0 0\n")
            automount_fstab.close()

        except:
            print("\n################################\n"
                  "Check the base installation commands.\n"
                  "################################\n")

        try:
            import RPi.GPIO as GPIO
            from mfrc522 import SimpleMFRC522
            os.system("ls /usr/local/lib/python3.9/dist-packages/mfrc522 | grep MFRC522")
            # moving the modfied RFID library to the library destination
            os.system(
                "sudo cp /home/pi/ServerFiles/Workflow/Workstation/modules/SimpleMFRC522.py "
                "/usr/local/lib/python3.9/dist-packages/mfrc522/")
            time.sleep(2)
        except ImportError:
            print("\n################################\n"
                  "Installing RFID packages...\n"
                  "################################\n")
            os.system("sudo apt-get -y install python3-dev python3-pip")
            os.system("sudo pip3 install spidev")
            os.system("sudo pip3 install mfrc522")
            os.system("ls /usr/local/lib/python3.9/dist-packages/mfrc522 | grep MFRC522")
            # moving the modfied RFID library to the library destination
            os.system(
                "sudo cp /home/pi/ServerFiles/Workflow/Workstation/modules/SimpleMFRC522.py "
                "/usr/local/lib/python3.9/dist-packages/mfrc522/")

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
            import ttkthemes
            from PIL import Image, ImageTk
        except ImportError:
            print("\n################################\n"
                  "Installing tkinter packages...\n"
                  "################################\n")
            os.system("sudo apt-get -y install python3-pil python3-pil.imagetk")
            os.system("python3 -m pip install git+https://github.com/RedFantom/ttkthemes")
            import _tkinter
            import tkinter
            import ttkthemes
            from PIL import Image, ImageTk

        try:
            print("\n################################\n"
                  "Setup of autonomic WorkstationApp start at launch...\n"
                  "################################\n")
            time.sleep(2)

            os.system("cd /home/pi/ServerFiles/Workflow/Workstation/")
            os.system(
                "echo \"#!/bin/bash\necho \"WorkstationApp wird in 5s gestartet...\"\nsleep 5\ncd /home/pi/ServerFiles/Workflow/Workstation\npython3 WorkstationApp.py"
                "\ncd /\" > /home/pi/ServerFiles/Workflow/Workstation/WorkstationLauncher.sh")
            os.system("sudo chmod 755 /home/pi/ServerFiles/Workflow/Workstation/WorkstationLauncher.sh")

            os.system("cd /home/pi/ServerFiles/Workflow/WorkflowPlanner/")
            os.system(
                "echo \"#!/bin/bash\necho \"WorkflowPlanner wird in 5s gestartet...\"\nsleep 5\ncd /home/pi/ServerFiles/Workflow/WorkflowPlanner\npython3 WorkflowPlannerApp.py"
                "\ncd /\" > /home/pi/ServerFiles/Workflow/WorkflowPlanner/WorkflowPlannerLauncher.sh")
            os.system("sudo chmod 755 /home/pi/ServerFiles/Workflow/WorkflowPlanner/WorkflowPlannerLauncher.sh")

            autostart_workstation_app = open("/etc/xdg/lxsession/LXDE-pi/autostart", "a")
            autostart_workstation_app.write(
                "@lxterminal -e bash /home/pi/ServerFiles/Workflow/Workstation/WorkstationLauncher.sh")
            autostart_workstation_app.close()

            os.system("cd /home/pi/Desktop/")
            os.system("echo \"[Desktop Entry]\n"
                      "Type=Application\n"
                      "Name=WorkstationApp\n"
                      "Terminal=true\n"
                      "Exec=/home/pi/ServerFiles/Workflow/Workstation/WorkstationLauncher.sh\n"
                      "Icon=/home/pi/ServerFiles/Logos/desktoplogo.png\n\" > /home/pi/Desktop/WorkstationApp.desktop")

            os.system("cd /home/pi/Desktop/")
            os.system("echo \"[Desktop Entry]\n"
                      "Type=Application\n"
                      "Name=WorkflowManager\n"
                      "Terminal=true\n"
                      "Exec=/home/pi/ServerFiles/Workflow/WorkflowPlanner/WorkflowPlannerLauncher.sh\n"
                      "Icon=/home/pi/ServerFiles/Logos/desktoplogo.png\n\" > /home/pi/Desktop/WorkflowPlannerApp.desktop")

            os.system("sudo rm /etc/xdg/lxsession/LXDE-pi/sshpwd.sh")

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
                  "Enter \"Y\" to reboot. It's necessary.\n"
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
