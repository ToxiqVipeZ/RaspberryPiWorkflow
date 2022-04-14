import sys
import tkinter as tk
from PIL import Image, ImageTk
import os


# constant variables
window_width = 1280
window_height = 720
confirm_button1_text = "Fertig"
confirm_button2_text = "Neustart"
progression_counter = 0
picture_type = ".png"
# end of constant variables


class Workflow(object):
    article_id = 0
    station = 0
    operation = 0
    variant = 0
    main_path = 0

    def __init__(self, argument):
        global progression_counter
        article_id = argument
        self.station = article_id[0:2]
        self.operation = article_id[2:5]
        self.variant = article_id[5:7]
        self.main_path = "C:/Users/g-oli/Desktop/Projekt ZF/Instruktionen/" \
                         + self.station + "/" + self.operation + "/"
        print(article_id)
        print(self.station)
        print(self.operation)
        print(self.variant)
        print(self.main_path)
        self.main()


    # image Size adjustment
    def workflow_picture_resize(self, workflow_pictures):
        if workflow_pictures.width > 720:
            size_matcher_width = workflow_pictures.width / 1280
            size_matcher_height = workflow_pictures.height / 720
            workflow_pictures = workflow_pictures.resize(
                (int(workflow_pictures.width / size_matcher_width),
                 int(workflow_pictures.height / size_matcher_height)))
        return workflow_pictures

    def change_picture(self):
        try:
            workflow_picture = Image.open(self.main_path + self.picture_progressor())
            workflow_picture = self.workflow_picture_resize(workflow_picture)
            # defining image as a photo image for tkinter
            workflow_picture = ImageTk.PhotoImage(workflow_picture)
            # label definition
            workflow_picture_label = tk.Label(image=workflow_picture)
            # insert image into label
            workflow_picture_label.image = workflow_picture
            # label position inside root2 grid
            workflow_picture_label.grid(column=0, row=0)
        except FileNotFoundError:
            print("\n Die Datei wurde nicht gefunden, sind alle Bilder \".png\" - Dateien ?")

    def folder_progressor(self):
        global picture_count
        file_names = os.listdir(self.main_path)
        for file_name in file_names:
            print(os.path.abspath(os.path.join(self.main_path, file_name)), sep="\n")
            picture_count = len(file_names)

    def picture_progressor(self):
        global progression_counter
        if progression_counter != picture_count:
            progression_counter += 1
            return str(progression_counter) + picture_type
        elif progression_counter == picture_count:
            print("Das war das letzte Bild")
            return str(progression_counter) + picture_type

    def hide_label(self):
        instruction_done.grid_forget()

    def workflow_completed(self, root2):
        if progression_counter == picture_count:
            #self.set_progression_counter(0)
            global instruction_done
            instruction_done = tk.Label(root2, text="Vorgang abgeschlossen", font="Arial")
            self.button_switcher(button1_btn, "disabled")
            instruction_done.grid(column=0, row=1)

    def button_switcher(self,button, status):
        button = button.configure(state=status)
        return button

    def set_picture_count(self, number):
        global picture_count
        picture_count = number

    def set_progression_counter(self, number):
        global progression_counter
        progression_counter = number

    def main(self):
        global button1_btn
        self.folder_progressor()

        # init of the window - START!
        root2 = tk.Tk()

        # window size
        canvas = tk.Canvas(root2, width=window_width, height=window_height)

        # window grid
        canvas.grid(columnspan=3, rowspan=3)

        # image definition as a image
        workflow_picture = Image.open(self.main_path + self.picture_progressor())

        # resizing the picture
        workflow_picture = self.workflow_picture_resize(workflow_picture)

        # defining image as a photo image for tkinter
        workflow_picture = ImageTk.PhotoImage(workflow_picture)
        # label definition
        workflow_picture_label = tk.Label(image=workflow_picture)
        # insert image into label
        workflow_picture_label.image = workflow_picture
        # label position inside root2 grid
        workflow_picture_label.grid(column=0, row=0)

        # instructions
        instructions = tk.Label(root2, text="Schritt " + str(progression_counter), font="Arial")
        instructions.grid(column=1, row=0)

        # button1 definition
        button1_text = tk.StringVar()
        button1_text.set(confirm_button1_text)
        button1_btn = tk.Button(root2, textvariable=button1_text,
                                command=lambda: (self.change_picture(), self.workflow_completed(root2)),
                                width=10, height=5, background="green")
        button1_btn.grid(column=1, row=0)

        # button2 definition
        button2_text = tk.StringVar()
        button2_text.set(confirm_button2_text)
        button2_btn = tk.Button(root2, textvariable=button2_text,
                                command=lambda: (self.set_progression_counter(0),
                                                 self.change_picture(),
                                                 self.button_switcher(button1_btn, "normal"),
                                                 self.hide_label()),
                                width=10, height=5, background="red")
        button2_btn.grid(column=2, row=0)

        # window size adjustment
        width, height = root2.winfo_screenwidth(), root2.winfo_screenheight()
        root2.geometry("%dx%d+0+0" % (width, height))

        # loop of the window - END!
        root2.mainloop()
