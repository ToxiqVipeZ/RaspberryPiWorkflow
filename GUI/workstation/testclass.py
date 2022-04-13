import workflowPagesDisplay
import tkinter as tk
from PIL import Image, ImageTk


class WaitForRFID(object):
    main_path = "C:/Users/g-oli/Desktop/Projekt ZF/Instruktionen/"
    rfid_in = "RFID-IN.png"
    rfid_out = "RFID-OUT.png"
    rfid_scanned = "0"

    def __init__(self, rfid_init):
        self.rfid_scanned = rfid_init
        self.main()

    def workflow_picture_resize(self, workflow_pictures):
        if workflow_pictures.width > 720:
            size_matcher_width = workflow_pictures.width / 1280
            size_matcher_height = workflow_pictures.height / 720
            workflow_pictures = workflow_pictures.resize(
                (int(workflow_pictures.width / size_matcher_width),
                 int(workflow_pictures.height / size_matcher_height)))
        return workflow_pictures

    def main(self):
        root = tk.Tk()
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()

        # window size
        canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        # window grid
        canvas.grid(columnspan=3, rowspan=3)

        # image definition as a image
        workflow_picture = Image.open(self.main_path + self.rfid_in)

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

        root.geometry("%dx%d+0+0" % (width, height))

        if self.rfid_scanned != 0:
            root.destroy()
            workflowPagesDisplay.Workflow(self.rfid_scanned)

        # loop of the window - END!
        root.mainloop()

    # workflowPagesDisplay.Workflow("rfid_in")


objectX = "I0100101"
objectX = objectX[1:]
WaitForRFID(objectX)
