import tkinter
from PIL import Image, ImageTk


def update_image(i, path, picture_number):
    global tkimg1
    tkimg1 = ImageTk.PhotoImage(Image.open(path + picture_number))
    label.config(image=tkimg1)
    label.after(1000, update_image(i, path, picture_number))
    i += 1
    print("Updated")


i = 1
path = "C:/Users/g-oli/Desktop/Projekt ZF/"

if i <= 2:
    picture_number = "A111" + str(i) + ".png"
if i == 3 or i == 4:
    picture_number = "A111" + str(i) + ".jpg"

window = tkinter.Tk()
im = Image.open(path + picture_number)
if (im.width > 720):
    size_matcher_width = im.width / 1280
    size_matcher_height = im.height / 720
    im = im.resize(
        (int(im.width / size_matcher_width), int(im.height / size_matcher_height)),
        Image.Resampling.LANCZOS)

tkimg1 = ImageTk.PhotoImage(im)
label = tkinter.Label(window, image=tkimg1)
print("Loaded")
label.pack()
window.after(1000, update_image(i, path, picture_number))
window.mainloop()
