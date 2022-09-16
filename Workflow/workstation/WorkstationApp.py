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
import time

try:
    import math
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
    import ttkthemes as ttk
except ImportError:
    print("ttkthemes import failed.")

try:
    from PIL import Image, ImageTk
except ImportError:
    print("PIL import failed.")

try:
    from modules import Client
except ImportError:
    print("Client import failed, check for correct file location.")


# C.O.S - Comment in:
# try:
#     from modules.WorkstationHandler import WorkstationHandler
# except ImportError:
#     print("WorkstationHandler import failed, check for correct file location.")


class WorkstationApp:
    """
    This class processes the RFID-Input from the RFID-Reader
    and shows related workflow steps.
    """
    # global variables:
    auto_width = 300
    auto_height = 220
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

    # static global variables:
    # C.O.S - Comment in:
    # MAIN_PATH_PRE = "/home/pi/WorkflowInstructions/"
    MAIN_PATH_PRE = "C:/Users/g-oli/Desktop/Projekt ZF/Instruktionen/"
    RFID_IN = "RFID-IN.png"
    RFID_OUT = "RFID-OUT.png"
    WINDOW_WIDTH = auto_width
    WINDOW_HEIGHT = auto_height
    CONFIRM_BUTTON_DONE_TEXT = "Fertig"
    CONFIRM_BUTTON_RESTART_TEXT = "Neustart"
    CONFIRM_BUTTON_ABORT_TEXT = "Ausschuss"
    ALARM_BUTTOM = "Alarm!"
    PICTURE_TYPE = ".png"

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
        self.main()

    def get_station_number(self):
        ip_address = str(Client.get_ip_address())
        this_station = ip_address.split(".")
        if this_station[2] != 0:
            if len(this_station[3]) == 1:
                this_station = "0" + str(this_station[3])
                return this_station
            if len(this_station[3]) == 2:
                this_station = str(this_station[3])
                return this_station
        else:
            print("Stations-IP hat keine \"1\" an der dritten Stelle.")

    def scanning_rfid(self):
        self.scan_flag = True
        self.rfid_scanned = ""
        work_handler = WorkstationHandler()
        work_handler.start_op("reader_start")
        self.rfid_scanned = work_handler.get_rfid()
        work_handler.reset_rfid()
        self.statistic_tracker("IN")
        self.scan_flag = False

    def statistic_tracker(self, in_or_out):
        station_number = self.get_station_number()
        print("statistic_tracker station_number: " + station_number)
        if in_or_out == "IN":
            Thread(target=Client.send(Client.TRACKING_STATS_IN, self.rfid_scanned, station_number)).start()
        elif in_or_out == "OUT":
            Thread(target=Client.send(Client.TRACKING_STATS_OUT, self.rfid_scanned, station_number)).start()

    def error_tracker(self, error_type, error_message):
        error_message = str(error_message) + "SplitStatement15121 01"

        # C.O.S - Comment in:
        # adds the station Number to the error_message:
        #error_message = str(error_message) + "SplitStatement15121 " + self.get_station_number()

        Thread(target=Client.send(Client.TRACKING_ERROR_IN, str(error_type), str(error_message))).start()
        self.error_solving(error_type, error_message)

    def error_solving(self, error_type, error_message):
        error_window = tk.Toplevel()
        error_window.geometry("%dx%d+0+0" % (error_window.winfo_screenwidth()/2, error_window.winfo_screenheight()/2))
        station = "01"
        # C.O.S Comment in:
        # station = self.get_station_number()

        error_type_picker_label = tk.Label(error_window,
                                           text="Error: \n\"" +
                                                error_type + "\"\n von Station: \n\"" +
                                                station +
                                                "\" \n behoben ?",
                                           font=("Arial Black", 15))
        # definition of the button
        solved_confirm_button = tk.Button(
            error_window,
            text="Ja, Fehler behoben.",
            command=lambda:
            (
                Client.send(Client.TRACKING_ERROR_OUT, str(error_type), str(error_message)), error_window.destroy()
            ),
            width=20,
            font=("Arial", 20)
        )

        error_type_picker_label.pack()
        solved_confirm_button.pack()

    def writing_rfid(self, rfid_scanned):
        work_handler = WorkstationHandler()
        work_handler.start_op("writer_start", rfid_scanned)
        work_handler.reset_rfid()
        self.statistic_tracker("OUT")
        self.set_progression_counter(0)
        self.written_flag = True

    def exec_after_scan(self):
        if self.rfid_scanned != "":
            self.rfid_readed(self.rfid_scanned)
        else:
            root.update()
            root.after(100, self.exec_after_scan)

    def alarm_button_pressed(self, root2):
        popup = tk.Toplevel(root2, )
        popup.state("zoomed")
        popup.geometry("%dx%d+0+0" % (popup.winfo_screenwidth(), popup.winfo_screenheight()))

        # window size
        canvas_root = tk.Canvas(popup, width=popup.winfo_screenwidth(), height=popup.winfo_screenheight())
        # window grid
        canvas_root.grid(columnspan=4, rowspan=4)
        error_list = Client.send(Client.GET_ERROR_LIST, "")
        error_list = error_list.split(";")
        print(error_list)
        # !!! FÜRS NÄCHSTE MAL: Daten müssen in Datenbank eingetragen werden !!!

        option_list = []
        range_limit = (len(error_list)) - 1
        counter = 0

        while counter in range(0, range_limit):
            option_list.append(error_list[counter] + ", " + error_list[counter + 1])
            counter += 2

        print(option_list)

        picked_option = tk.StringVar(popup)
        picked_option.set("Hier Klicken.")

        # spaceholder for button-alignment
        spaceholder1 = tk.Label(popup, width=10)

        # spaceholder for button-alignment
        spaceholder2 = tk.Label(popup, width=10)

        # definition of error type section
        error_type_picker_label = tk.Label(popup, text="Wähle Fehlertyp: ", font=("Arial Black", 30))
        error_type_picker = tk.OptionMenu(popup, picked_option, *option_list)
        error_type_picker.config(width=30, font=("Arial", 30))

        # definition of error comment section
        error_comment_label = tk.Label(popup, text="Beschreibe Fehler: ", font=("Arial Black", 30))

        error_comment_entry = tk.Text(popup, width=50, height=10, font=("Arial", 20))

        # definition of the button
        popup_confirm_button = tk.Button(
            popup,
            text="Absenden",
            command=lambda: (self.error_tracker(picked_option.get(), error_comment_entry.get("1.0", 'end-1c')),
                             popup.destroy()),
            width=30,
            font=("Arial", 20)
        )

        # integration into the scene and alignment
        spaceholder1.grid(column=0, rowspan=4)
        error_type_picker_label.grid(column=1, row=0)
        error_type_picker.grid(column=2, row=0)
        error_comment_label.grid(column=1, row=1)
        error_comment_entry.grid(column=2, row=1)
        popup_confirm_button.grid(column=2, row=2)
        spaceholder2.grid(column=3, rowspan=4)

    def workflow_picture_resize(self, workflow_pictures):
        """
        Takes one workflow picture and downscales it, if its > 720p
        :param workflow_pictures: one workflow picture
        :return: the given workflow picture after downscaling
        """
        self.WINDOW_WIDTH = self.auto_width
        self.WINDOW_HEIGHT = self.auto_height

        if workflow_pictures.width > 720 or self.auto_width < 720:
            size_matcher_width = workflow_pictures.width / (self.WINDOW_WIDTH * 0.8)
            size_matcher_height = workflow_pictures.height / (self.WINDOW_HEIGHT * 0.8)
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
            workflow_picture_label.grid(column=0, row=1, rowspan=4)
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
                print("RFID written!")
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
            root2.state("zoomed")

            # window size
            canvas = tk.Canvas(root2, width=root2.winfo_screenwidth(), height=root2.winfo_screenheight())
            canvas.config(borderwidth=0)

            # window grid
            canvas.grid(columnspan=2, rowspan=6)

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
            workflow_picture_label.config(borderwidth=0)

            # C.O.S - Comment in, Delete next:
            #station_label = tk.Label(root2, text=self.get_station_number(), font=("Arial Black", 30))
            station_label = tk.Label(root2, text="Station 01", font=("Arial Black", 30))
            station_label.grid(column=0, row=0)

            # label position inside root2 grid
            workflow_picture_label.grid(column=0, row=1, rowspan=4)

            # spaceholder for button-alignment
            #spaceholder_picture_buttons = tk.Label(root2, height=1)

            # button1 definition
            button1_text = tk.StringVar()
            button1_text.set(self.CONFIRM_BUTTON_DONE_TEXT)
            button1_btn = tk.Button(root2, textvariable=button1_text,
                                    command=lambda: (self.workflow_completed(root2),
                                                     self.change_picture(root2, self.picture_progressor(root2))),
                                    width=10, height=5, background="green")
            button1_btn.grid(column=1, row=1)

            # button2 definition
            button2_text = tk.StringVar()
            button2_text.set(self.CONFIRM_BUTTON_RESTART_TEXT)
            button2_btn = tk.Button(root2, textvariable=button2_text,
                                    command=lambda: (self.set_progression_counter(0),
                                                     self.change_picture(root2, self.picture_progressor(root2)),
                                                     self.button_switcher(button1_btn, "normal")),
                                    width=10, height=5, background="yellow")
            button2_btn.grid(column=1, row=2)

            # button3 definition
            button3_text = tk.StringVar()
            button3_text.set(self.CONFIRM_BUTTON_ABORT_TEXT)
            button3_btn = tk.Button(root2, textvariable=button3_text,
                                    command=lambda: (self.ausschuss_prozess(root2)),
                                    width=10, height=5, background="orange")
            button3_btn.grid(column=1, row=3)

            # button4 definition
            button4_text = tk.StringVar()
            button4_text.set(self.ALARM_BUTTOM)
            button4_btn = tk.Button(root2, textvariable=button4_text,
                                    command=lambda: (self.alarm_button_pressed(root2)),
                                    width=10, height=5, background="red")
            button4_btn.grid(column=1, row=4)

            #spaceholder_picture_buttons.grid(column=1, row=0)

            # window size adjustment
            width, height = root2.winfo_screenwidth(), root2.winfo_screenheight()
            root2.geometry("%dx%d+0+0" % (width, height))

            # loop of the window - END!
            root2.mainloop()
        except FileNotFoundError:
            print("Datei nicht gefunden, bitte überprüfen ob Pfad angelegt ist.")
            root.after(3000, Thread(target=self.scanning_rfid).start())
            root.after(5000, self.exec_after_scan)

    # C.O.S - Delete after test:
    def test(self):
        self.rfid_scanned = "01001-01"

    def main(self):
        """
        the main window, only showing and waiting for an RFID-chip to get read
        """
        try:
            global root
            root = tk.Tk()
            root.state("zoomed")
            self.auto_width = root.winfo_screenwidth()
            self.auto_height = root.winfo_screenheight()

            #width, height = root.winfo_screenwidth(), root.winfo_screenheight()

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

            root.geometry("%dx%d+0+0" % (self.auto_width, self.auto_height))

            # C.O.S - Comment in, Delete next:
            # station_label = tk.Label(root, text=self.get_station_number(), font=("Arial Black", 30))
            station_label = tk.Label(root, text="Station 01", font=("Arial Black", 30))
            station_label.grid(column=1, row=0)

            # C.O.S - Delete:
            # button1 definition
            button1_text = tk.StringVar()
            button1_text.set("TestB")
            button1_btn = tk.Button(root, textvariable=button1_text,
                                    command=lambda: (self.test()),
                                    width=10, height=5, background="green")
            button1_btn.grid(column=1, row=1)
            # C.O.S - Comment in:
            # root.after(1000, Thread(target=self.scanning_rfid).start())
            root.after(1000, self.exec_after_scan)

            # loop of the window - END!
            root.mainloop()
        finally:
            Client.send(Client.DISCONNECT_MESSAGE)
            exit()


if __name__ == "__main__":
    WorkstationApp()
