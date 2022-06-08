"""
Import list:
    WorkstationApp:
        import os
        from threading import Thread
        import _tkinter
        import tkinter as tk
        from PIL import Image, ImageTk
        from modules import Client
        from modules.WorkstationHandler import WorkstationHandler
    WorkstationHandler:
        import modules.Reader import Reader
        from modules.Writer import Writer
        from threading import Thread
    Reader:
        import RPi.GPIO as GPIO
        from mfrc522 import SimpleMFRC522
        from threading import Thread
        import time
    Writer:
        import RPi.GPIO as GPIO
        from mfrc522 import SimpleMFRC522
        import time
    Client:
        import socket

Other OS related:
    Fileserver link:
        mkdir /home/pi/Desktop/Fileserver
        sudo mount -t cifs -o username=pi,password=raspberry //169.254.0.2/WorkflowInstructions /home/pi/Desktop/Fileserver
        sudo chmod -R 777 /home/pi/Desktop/Fileserver
        
        os.system("sudo apt-get update")
        os.system("sudo apt-get upgrade")
        os.system("sudo apt-get -y install libjpeg-dev zlib1g-dev libfreetype6-dev liblcms1-dev libopenjp2-7 libtiff5")
"""

try:
    import os
    from threading import Thread
except ImportError:
    print("Baseimports failed - check os and threading.")

try:
    import _tkinter
except ImportError:
    print("_tkinter import failed.")

try:
    import tkinter as tk
except ImportError:
    print("tkinter import failed.")

try:
    from PIL import Image, ImageTk
except ImportError:
    print("PIL import failed.")

try:
    from modules import Client
except ImportError:
    print("Client import failed, check for correct file location.")

try:
    from modules.WorkstationHandler import WorkstationHandler
except ImportError:
    print("WorkstationHandler import failed, check for correct file location.")


class WorkstationApp:
    """
    This class processes the RFID-Input from the RFID-Reader
    and shows related workflow steps.
    """
    # static global variables:
    MAIN_PATH_PRE = "/home/pi/WorkflowInstructions/"
    RFID_IN = "RFID-IN.png"
    RFID_OUT = "RFID-OUT.png"
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    CONFIRM_BUTTON_DONE_TEXT = "Fertig"
    CONFIRM_BUTTON_RESTART_TEXT = "Neustart"
    CONFIRM_BUTTON_ABORT_TEXT = "Ausschuss"
    PICTURE_TYPE = ".png"

    # global variables:
    rfid_scanned = ""
    station = 0
    operation = 0
    variant = 0
    main_path = "0"
    progression_counter = 0
    picture_count = 0
    new_rfid = ""
    written_flag = False
    scan_flag = False
    ausschuss_procedure = False

    def workflow_start(self, argument):
        """
        Starts the workflow-steps
        :param argument: given rfid-id
        """
        self.set_progression_counter(0)
        self.set_picture_count(0)
        self.rfid_scanned = argument
        article_id = argument
        self.station = article_id[0:2]
        self.operation = article_id[2:5]
        self.variant = article_id[5:]
        self.main_path = self.MAIN_PATH_PRE + self.station + "/" + self.operation + "/"
        print(article_id)
        print(self.station)
        print(self.operation)
        print(self.variant)
        print(self.main_path)
        self.second_window()

    def __init__(self):
        """
        Initialisation method
        """
        # T1 = Thread(target=self.main()).start()
        # T2 = Thread(target=self.scanning_rfid()).start()
        self.main()

    def scanning_rfid(self):
        self.scan_flag = True
        self.rfid_scanned = ""
        work_handler = WorkstationHandler()
        work_handler.start_op("reader_start")
        self.rfid_scanned = work_handler.get_rfid()
        work_handler.reset_rfid()
        self.scan_flag = False

    def writing_rfid(self, rfid_scanned):
        work_handler = WorkstationHandler()
        work_handler.start_op("writer_start", rfid_scanned)
        work_handler.reset_rfid()
        self.set_progression_counter(0)
        self.written_flag = True

    def exec_after_scan(self):
        if self.rfid_scanned != "":
            self.rfid_readed(self.rfid_scanned)
        else:
            root.update()
            root.after(100, self.exec_after_scan)

    def workflow_picture_resize(self, workflow_pictures):
        """
        Takes one workflow picture and downscales it, if its > 720p in height
        :param workflow_pictures: one workflow picture
        :return: the given workflow picture after downscaling
        """
        if workflow_pictures.width > 720:
            size_matcher_width = workflow_pictures.width / 1280
            size_matcher_height = workflow_pictures.height / 720
            workflow_pictures = workflow_pictures.resize(
                (int(workflow_pictures.width / size_matcher_width),
                 int(workflow_pictures.height / size_matcher_height)))
        return workflow_pictures

    def change_picture(self, root, picture):
        """
        Switches Pictures inside a given window
        :param root: given window
        :param picture: picture to switch to
        """
        try:
            workflow_picture = Image.open(self.main_path + picture)
            workflow_picture = self.workflow_picture_resize(workflow_picture)
            # defining image as a photo image for tkinter
            workflow_picture = ImageTk.PhotoImage(workflow_picture)
            # label definition
            workflow_picture_label = tk.Label(root, image=workflow_picture)
            # insert image into label
            workflow_picture_label.image = workflow_picture
            # label position inside root grid
            workflow_picture_label.grid(column=0, row=0, rowspan=3)
        except FileNotFoundError:
            print("\n Die Datei wurde nicht gefunden, sind alle Bilder \".png\" - Dateien ?")
        except _tkinter.TclError:
            self.progression_counter = 0
            print("second screen destroyed, returning to root screen(RFID-IN)")
            root.after(3000, Thread(target=self.scanning_rfid).start())
            root.after(5000, self.exec_after_scan)

    def folder_progressor(self):
        """
        progresses trough the folders and sets the amount of pictures in given folder
        """
        if self.rfid_scanned != "no next station":
            # putting all filenames from the main_path direction into file_names
            file_names = os.listdir(self.main_path)
            # setting the amount of pictures to progress trough based on the filenames
            self.set_picture_count(len(file_names))

            # looking, which of the file_names are ending with a "_v" and exclude them from picture count
            for file_name in file_names:
                print(os.path.abspath(os.path.join(self.main_path, file_name)), sep="\n")
                if file_name.endswith("_v"):
                    self.picture_count -= 1

    def picture_progressor(self, root2):
        """
        - progresses trough the pictures inside a given folder
        - if a file is tagged by "_v", it will browse the folder with the same number
            as the file, that contains "_v" and pics the right variation
        :return: the next picture in folder
        """
        try:
            if self.rfid_scanned != "no next station":
                alternative = ""
                # saving all filenames
                file_names = os.listdir(self.main_path)
                print(self.variant)
                # looking if progression counter is not at the last picture to increment it
                if self.progression_counter != self.picture_count:
                    self.progression_counter += 1

                    # looking if there is a variation number given
                    if self.variant != "00":
                        alternative = str(self.progression_counter) + self.PICTURE_TYPE
                        alternative = alternative.replace("/", "\\")

                        # looking if it is needed to go into a variation folder
                        if (alternative not in file_names):
                            return str(self.progression_counter) + "_v/" + self.variant + self.PICTURE_TYPE
                        elif (alternative in file_names):
                            return str(self.progression_counter) + self.PICTURE_TYPE

                    # looking if there is no variation number given:
                    elif self.variant == "00":
                        alternative = str(self.progression_counter) + self.PICTURE_TYPE
                        alternative = alternative.replace("/", "\\")

                        # if no variation number, then the default picture will be given back
                        if (alternative not in file_names):
                            return str(self.progression_counter) + "_v" + self.PICTURE_TYPE
                        elif (alternative in file_names):
                            return str(self.progression_counter) + self.PICTURE_TYPE

                # looking if the progression counter is at the last picture
                elif self.progression_counter >= self.picture_count:
                    print("Das war das letzte Bild")
                    self.workflow_completed(root2)
                    return str(self.progression_counter) + self.PICTURE_TYPE

        except FileNotFoundError:
            self.scan_flag = True
            print("Datei nicht gefunden, bitte überprüfen ob Pfad angelegt ist.")
            root.after(3000, Thread(target=self.scanning_rfid).start())
            root.after(5000, self.exec_after_scan)

    def workflow_completed(self, root2):
        """
        destroys the workflow window, when "Fertig" is pressed after the last picture
        :param root2: the workflow window
        """
        if not self.ausschuss_procedure:
            if self.progression_counter >= self.picture_count:
                root.update()
                root2.update()
                self.rfid_submit(root2)
                print("RFID already written!")
                root2.destroy()
        else:
            root2.update()
            root2.destroy()

    def ausschuss_prozess(self, root2):
        """
        executes when the "Ausschuss"-Button is pressed, destroys the workflow window
        resets the progression counter
        :param root2: the workflow window
        """
        self.ausschuss_procedure = True
        self.workflow_completed(root2)
        self.ausschuss_procedure = False
        self.set_progression_counter(0)
        if self.scan_flag == False:
            root.after(3000, Thread(target=self.scanning_rfid).start())
            root.after(5000, self.exec_after_scan)

    def button_switcher(self, button, status):
        """
        switches the state of a button, currently unused
        :param button: a button object
        :param status: a state <disabled, active, normal>
        :return: the button object
        """
        button = button.configure(state=status)
        return button

    def set_picture_count(self, number):
        """
        sets the number of given pictures in a folder
        :param number: the picture count
        """
        self.picture_count = number

    def set_progression_counter(self, number):
        """
        sets the actual number of which picture to look at, equals the picture number
        :param number: picture number
        """
        self.progression_counter = number

    def rfid_submit(self, root2):
        self.written_flag = False
        print("Old RFID: " + self.rfid_scanned)
        self.new_rfid = Client.send(Client.SENDING_RFID, self.rfid_scanned)
        self.rfid_scanned = self.new_rfid + self.operation + self.variant
        print("New RFID: " + self.rfid_scanned)
        root2.update()
        if not self.written_flag:
            root.after(1, Thread(target=self.rfid_writer(self.rfid_scanned)).start())
            while not self.written_flag:
                root.update()
                root2.update()

    # finally:
    #    # client disconnects from the server
    #    Client.send(Client.DISCONNECT_MESSAGE)

    def rfid_readed(self, rfid_scan):
        self.workflow_start(rfid_scan)

    def rfid_writer(self, rfid_scanned):
        root.after(1000, Thread(target=self.writing_rfid(rfid_scanned)).start())
        root.after(1500)

    def second_window(self):
        """
        the method, that creates the workflow window
        :return:
        """
        global button1_btn
        try:
            self.folder_progressor()

            # init of the window - START!
            root2 = tk.Toplevel()

            # window size
            canvas = tk.Canvas(root2, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT)
            # window grid
            canvas.grid(columnspan=3, rowspan=3)

            # image definition as a image
            workflow_picture = Image.open(self.main_path + self.picture_progressor(root2))
            # resizing the picture
            workflow_picture = self.workflow_picture_resize(workflow_picture)
            # defining image as a photo image for tkinter
            workflow_picture = ImageTk.PhotoImage(workflow_picture)
            # label definition
            workflow_picture_label = tk.Label(root2, image=workflow_picture)
            # insert image into label
            workflow_picture_label.image = workflow_picture
            # label position inside root2 grid
            workflow_picture_label.grid(column=0, row=0, rowspan=3)

            # spaceholder for button-alignment
            spaceholder_picture_buttons = tk.Label(root2, width=10, height=20)
            spaceholder_picture_buttons.grid(column=1, row=0)

            # button1 definition
            button1_text = tk.StringVar()
            button1_text.set(self.CONFIRM_BUTTON_DONE_TEXT)
            button1_btn = tk.Button(root2, textvariable=button1_text,
                                    command=lambda: (self.workflow_completed(root2),
                                                     self.change_picture(root2, self.picture_progressor(root2))),
                                    width=10, height=5, background="green")
            button1_btn.grid(column=2, row=0)

            # button2 definition
            button2_text = tk.StringVar()
            button2_text.set(self.CONFIRM_BUTTON_RESTART_TEXT)
            button2_btn = tk.Button(root2, textvariable=button2_text,
                                    command=lambda: (self.set_progression_counter(0),
                                                     self.change_picture(root2, self.picture_progressor(root2)),
                                                     self.button_switcher(button1_btn, "normal")),
                                    width=10, height=5, background="yellow")
            button2_btn.grid(column=2, row=1)

            # button3 definition
            button3_text = tk.StringVar()
            button3_text.set(self.CONFIRM_BUTTON_ABORT_TEXT)
            button3_btn = tk.Button(root2, textvariable=button3_text,
                                    command=lambda: (self.ausschuss_prozess(root2)),
                                    width=10, height=5, background="red")
            button3_btn.grid(column=2, row=2)

            # window size adjustment
            width, height = root2.winfo_screenwidth(), root2.winfo_screenheight()
            root2.geometry("%dx%d+0+0" % (width, height))

            # loop of the window - END!
            root2.mainloop()
        except FileNotFoundError:
            print("Datei nicht gefunden, bitte überprüfen ob Pfad angelegt ist.")
            root.after(3000, Thread(target=self.scanning_rfid).start())
            root.after(5000, self.exec_after_scan)

    def main(self):
        """
        the main window, only showing and waiting for an RFID-chip to get read
        """
        try:
            global root
            root = tk.Tk()
            width, height = root.winfo_screenwidth(), root.winfo_screenheight()

            # window size
            canvas_root = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
            # window grid
            canvas_root.grid(columnspan=3, rowspan=3)

            # image definition as a image
            workflow_picture_root = Image.open(self.MAIN_PATH_PRE + self.RFID_IN)
            # resizing the picture
            workflow_picture_root = self.workflow_picture_resize(workflow_picture_root)
            # defining image as a photo image for tkinter
            workflow_picture_root = ImageTk.PhotoImage(workflow_picture_root)
            # label definition
            workflow_picture_root_label = tk.Label(image=workflow_picture_root)
            # insert image into label
            workflow_picture_root_label.image = workflow_picture_root
            # label position inside root grid
            workflow_picture_root_label.grid(column=0, row=0)

            root.geometry("%dx%d+0+0" % (width, height))

            root.after(1000, Thread(target=self.scanning_rfid).start())
            root.after(1000, self.exec_after_scan)
            # root.after(5000, self.check_scan)
            # loop of the window - END!
            root.mainloop()
        finally:
            Client.send(Client.DISCONNECT_MESSAGE)
            exit()


if __name__ == "__main__":
    WorkstationApp()
