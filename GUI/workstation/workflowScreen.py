import tkinter as tk
from PIL import Image, ImageTk
import time


global i
i = 1
global workflow_pictures

class Gui:


    def main(self):
        print("test")
        picture_number = " "
        print("C:/Users/g-oli/Desktop/Projekt ZF/" + picture_number)
        self.draw_window()


    def update_image(self, label, path, picture_number):
        workflow_pictures = ImageTk.PhotoImage(Image.open(path + picture_number))
        label.config(image=workflow_pictures)
        label.after(2000, self.update_image(label, path, picture_number))
        print("Updated")
        i += 1

    def draw_window(self):
        if i <= 2:
            picture_number = "A111" + str(i) + ".png"
        if i == 3 or i == 4:
            picture_number = "A111" + str(i) + ".jpg"

        path = "C:/Users/g-oli/Desktop/Projekt ZF/"
        main_window = tk.Tk()
        canvas = tk.Canvas(main_window, width=1280, height=720)
        canvas.grid(columnspan=3)

        workflow_pictures = Image.open(path + picture_number)
        workflow_pictures = workflow_pictures.resize(
            (int(workflow_pictures.width / 1.1), int(workflow_pictures.height / 1.1)), Image.Resampling.LANCZOS)

        #Image Size adjustment
        if (workflow_pictures.width > 720):
            size_matcher_width = workflow_pictures.width / 1280
            size_matcher_height = workflow_pictures.height / 720
            workflow_pictures = workflow_pictures.resize(
                (int(workflow_pictures.width / size_matcher_width), int(workflow_pictures.height / size_matcher_height)), Image.Resampling.LANCZOS)

        workflow_pictures = ImageTk.PhotoImage(workflow_pictures)
        workflow_pictures_label = tk.Label(image=workflow_pictures)
        workflow_pictures_label.image = workflow_pictures
        workflow_pictures_label.grid(column=1, row=0)
        main_window.after(2000, self.update_image(workflow_pictures_label, path, picture_number))
        #Check: https://bytes.com/topic/python/answers/933486-tkinter-reloading-window-displaying-image
        main_window.mainloop()




Gui().main()
