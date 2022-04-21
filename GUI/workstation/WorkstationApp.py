import _tkinter
import tkinter as tk
from PIL import Image, ImageTk
import os


class WorkstationApp(object):
    """
    This class processes the RFID-Input from the RFID-Reader
    and shows related workflow steps.
    """
    # static global variables:
    MAIN_PATH_PRE = "C:/Users/g-oli/Desktop/Projekt ZF/Instruktionen/"
    RFID_IN = "RFID-IN.png"
    RFID_OUT = "RFID-OUT.png"
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    CONFIRM_BUTTON_DONE_TEXT = "Fertig"
    CONFIRM_BUTTON_RESTART_TEXT = "Neustart"
    CONFIRM_BUTTON_ABORT_TEXT = "Ausschuss"
    PICTURE_TYPE = ".png"

    # global variables:
    rfid_scanned = "0"
    article_id = 0
    station = 0
    operation = 0
    main_path = "0"
    progression_counter = 0
    rfid_out_trigger = 0

    def workflow_start(self, argument):
        """
        Starts the workflow-steps
        :param argument: given rfid-id
        """
        article_id = argument
        self.station = article_id[0:2]
        self.operation = article_id[2:5]
        self.main_path = self.MAIN_PATH_PRE + self.station + "/" + self.operation + "/"
        print(article_id)
        print(self.station)
        print(self.operation)
        print(self.main_path)
        self.second_window()

    def __init__(self, rfid_init):
        """
        Initialisation method
        :param rfid_init: saves the RFID on object creation or class call in rfid_scanned
        """
        self.rfid_scanned = rfid_init
        self.main()

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

    def folder_progressor(self):
        """
        progresses trough the folders and sets the amount of pictures in given folder
        """
        file_names = os.listdir(self.main_path)
        for file_name in file_names:
            print(os.path.abspath(os.path.join(self.main_path, file_name)), sep="\n")
            self.set_picture_count(len(file_names))

    def picture_progressor(self):
        """
        progresses trough the pictures inside a given folder
        :return: the next picture in folder
        """
        try:
            if self.progression_counter != self.picture_count:
                self.progression_counter += 1
                return str(self.progression_counter) + self.PICTURE_TYPE
            elif self.progression_counter == self.picture_count:
                print("Das war das letzte Bild")
                return str(self.progression_counter) + self.PICTURE_TYPE
        except FileNotFoundError:
            print("Datei nicht gefunden, bitte überprüfen ob Pfad angelegt ist.")

    def workflow_completed(self, root2):
        """
        destroys the workflow window, when "Fertig" is pressed after the last picture
        :param root2: the workflow window
        """
        if self.progression_counter == self.picture_count:
            root2.destroy()

    def ausschuss_prozess(self, root2):
        """
        executes when the "Ausschuss"-Button is pressed, destroys the workflow window
        resets the progression counter
        :param root2: the workflow window
        """
        self.set_progression_counter(0)
        root2.destroy()

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
            workflow_picture = Image.open(self.main_path + self.picture_progressor())
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
                                                     self.change_picture(root2, self.picture_progressor())),
                                    width=10, height=5, background="green")
            button1_btn.grid(column=2, row=0)

            # button2 definition
            button2_text = tk.StringVar()
            button2_text.set(self.CONFIRM_BUTTON_RESTART_TEXT)
            button2_btn = tk.Button(root2, textvariable=button2_text,
                                    command=lambda: (self.set_progression_counter(0),
                                                     self.change_picture(root2, self.picture_progressor()),
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

    def main(self):
        """
        the main window, only showing and waiting for an RFID-chip to get read
        """
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

        # buttonTest definition
        buttonTest_text = tk.StringVar()
        buttonTest_text.set("Test")
        buttonTest_btn = tk.Button(root, textvariable=buttonTest_text,
                                   command=lambda: (self.workflow_start(self.rfid_scanned)),
                                   width=10, height=5, background="green")
        buttonTest_btn.grid(column=1, row=0)

        # loop of the window - END!
        root.mainloop()


# example of calling this class
objectX = "I01001"
objectX = objectX[1:]
WorkstationApp(objectX)
