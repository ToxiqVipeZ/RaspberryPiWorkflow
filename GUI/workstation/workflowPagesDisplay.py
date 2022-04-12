import tkinter as tk
from PIL import Image, ImageTk
import os


# constant variables
window_width = 1280
window_height = 720
confirm_button1_text = "Fertig"
confirm_button2_text = "Neustart"
picture_count = 3
progression_counter = 0
station = "Fertigung"
picture_type = ".png"
instruction = "Instruktion"
main_path = "C:/Users/g-oli/Desktop/Projekt ZF/Instruktionen/" + station + "/"
# end of constant variables


class Workflow:

    def __init__(self, article_id):
        pass

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
            workflow_picture = Image.open(main_path + self.picture_progressor())
            workflow_picture = self.workflow_picture_resize(workflow_picture)
            # defining image as a photo image for tkinter
            workflow_picture = ImageTk.PhotoImage(workflow_picture)
            # label definition
            workflow_picture_label = tk.Label(image=workflow_picture)
            # insert image into label
            workflow_picture_label.image = workflow_picture
            # label position inside root grid
            workflow_picture_label.grid(column=0, row=0)
        except FileNotFoundError:
            print("\n Die Datei wurde nicht gefunden, sind alle Bilder \".png\" - Dateien ?")

    def folder_progressor(self):
        global main_path
        global picture_count
        file_names = os.listdir(main_path)
        for file_name in file_names:
            print(os.path.abspath(os.path.join(main_path, file_name)), sep="\n")
            picture_count = len(file_names)

    def picture_progressor(self):
        global progression_counter
        if progression_counter != picture_count:
            progression_counter += 1
            return station + instruction + str(progression_counter) + picture_type
        elif progression_counter == picture_count:
            print("Das war das letzte Bild")
            return station + instruction + str(progression_counter) + picture_type

    def workflow_completed(self, root):
        if progression_counter == picture_count:
            self.set_progression_counter(0)
            instruction_done = tk.Label(root, text="Vorgang abgeschlossen", font="Arial")
            instruction_done.grid(column=0, row=1)

    def set_picture_count(self, number):
        global picture_count
        picture_count = number

    def set_progression_counter(self, number):
        global progression_counter
        progression_counter = number

    def main(self):
        self.folder_progressor()
        # init of the window - START!
        root = tk.Tk()

        # window size
        canvas = tk.Canvas(root, width=window_width, height=window_height)
        # window grid
        canvas.grid(columnspan=3, rowspan=3)

        # image definition as a image
        workflow_picture = Image.open(main_path + self.picture_progressor())

        # resizing the picture
        workflow_picture = self.workflow_picture_resize(workflow_picture)

        # defining image as a photo image for tkinter
        workflow_picture = ImageTk.PhotoImage(workflow_picture)
        # label definition
        workflow_picture_label = tk.Label(image=workflow_picture)
        # insert image into label
        workflow_picture_label.image = workflow_picture
        # label position inside root grid
        workflow_picture_label.grid(column=0, row=0)

        # instructions
        instructions = tk.Label(root, text="Schritt " + str(progression_counter), font="Arial")
        instructions.grid(column=1, row=0)

        # button1 definition
        button1_text = tk.StringVar()
        button1_text.set(confirm_button1_text)
        button1_btn = tk.Button(root, textvariable=button1_text,
                                command=lambda: (self.change_picture(), self.workflow_completed(root)),
                                width=10, height=5)
        button1_btn.grid(column=1, row=0)
        button1_btn.configure(background="green")

        # button2 definition
        button2_text = tk.StringVar()
        button2_text.set(confirm_button2_text)
        button2_btn = tk.Button(root, textvariable=button2_text,
                                command=lambda: (self.set_progression_counter(0), self.change_picture()),
                                width=10, height=5)
        button2_btn.grid(column=2, row=0)
        button2_btn.configure(background="red")

        # loop of the window - END!
        root.mainloop()


Workflow("test").main()
