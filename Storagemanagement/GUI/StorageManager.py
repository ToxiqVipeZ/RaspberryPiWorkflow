import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

from Storagemanagement.Backend.StorageManagerBackend import StorageManagerBackend


class StorageManager:
    Backend = StorageManagerBackend()

    def __init__(self):
        self.main()

    def treeview_creator(self, root, database_lookup_box):
        columns = ("article_id", "part_ids", "part_amounts")

        data = self.Backend.lookup_article_parts_relations(database_lookup_box)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=("Arial Black", 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=("Arial Black", 12, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        tree = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview")

        tree.column("article_id", anchor="center")
        tree.column("part_ids", anchor="center")
        tree.column("part_amounts", anchor="center")

        tree.heading("article_id", text="Artikel ID:")
        tree.heading("part_ids", text="Teile-ID:")
        tree.heading("part_amounts", text="Menge:")

        article_id = data[0]

        splitted_parts = (data[1].split("\', \'"))
        splitted_parts[0] = splitted_parts[0][2:]
        splitted_parts[len(splitted_parts)-1] = splitted_parts[len(splitted_parts)-1][:-2]

        split_part_amounts = (data[2].split("\', \'"))
        split_part_amounts[0] = split_part_amounts[0][2:]
        split_part_amounts[len(split_part_amounts)-1] = split_part_amounts[len(split_part_amounts)-1][:-2]

        for x in range(0, len(split_part_amounts)):
            print(splitted_parts[x], split_part_amounts[x])
            tree.insert("", tk.END, values=(" ", splitted_parts[x], split_part_amounts[x]))

        tree.insert("", 0, values=article_id)
        tree.grid(column=4, row=4)
        root.update()


    def feedback_label(self, root, message):
        message_label = tk.Label(root,
                                 text=message,
                                 background="grey",
                                 font=("Arial Black", 15))
        message_label.grid(column=2, row=9)
        root.update()
        self.Backend.delayed_destroyer(message_label, 2)


    def main(self):
        try:
            # loop of the window - START!
            root = tk.Tk()

            # window size:
            width, height = root.winfo_screenwidth(), root.winfo_screenheight()
            root.geometry("%dx%d+0+0" % (width, height))
            # background:
            canvas = tk.Canvas(root, width=width, height=height, background="grey")
            canvas.config(borderwidth=0)
            # window grid:
            canvas.grid(columnspan=5, rowspan=10)

            # label definition:
            article_id_box_label = tk.Label(root,
                                            text="Artikel-ID:",
                                            background="grey",
                                            font=("Arial Black", 15))
            part_numbers_box_label = tk.Label(root,
                                              text="Teilenummern x Menge: (Bsp.: 015231x7)",
                                              background="grey",
                                              font=("Arial Black", 15))
            article_id_delete_label = tk.Label(root,
                                               text="Artikel-ID löschen:",
                                               background="grey",
                                               font=("Arial Black", 15))
            database_lookup_label = tk.Label(root,
                                               text="Artikel-ID suchen:",
                                               background="grey",
                                               font=("Arial Black", 15))

            # when the save button is pressed, take_input gets called
            button_save_btn = tk.Button(root, text="Speichern",
                                        command=lambda: (
                                            self.Backend.save_article_parts_relations(
                                                article_id_box,
                                                part_numbers_box
                                            ),
                                            self.feedback_label(root, self.Backend.feedback_message)
                                        ),
                                        width=8, height=1, background="green", font=("Arial", 14))

            button_delete_btn = tk.Button(root, text="Löschen",
                                          command=lambda: (
                                              self.Backend.delete_article_parts_relations(
                                                  article_id_delete_box
                                              ),
                                              self.feedback_label(root, self.Backend.feedback_message)
                                          ),
                                          width=8, height=1, background="green", font=("Arial", 14))

            database_lookup_btn = tk.Button(root, text="Löschen",
                                          command=lambda: (
                                              self.treeview_creator(root, database_lookup_box),
                                              self.feedback_label(root, self.Backend.feedback_message)
                                          ),
                                          width=8, height=1, background="green", font=("Arial", 14))



            article_id_box = tk.Text(root, height=1, width=50)
            part_numbers_box = tk.Text(root, height=20, width=50)
            column_0_width = tk.Canvas(width=width/3, height=1)

            column_0_width.grid(column=0, row=0)
            article_id_box_label.grid(column=0, row=1)
            article_id_box.grid(column=0, row=2)
            part_numbers_box_label.grid(column=0, row=3)
            part_numbers_box.grid(column=0, row=4)
            button_save_btn.grid(column=0, row=5)

            article_id_delete_box = tk.Text(root, height=1, width=50)
            placeholder_col_0to2 = tk.Canvas(background="black", width=2, height=height)
            column_2_width = tk.Canvas(width=width / 3, height=1)

            column_2_width.grid(column=2, row=0)
            placeholder_col_0to2.grid(column=1, row=0, rowspan=20)
            article_id_delete_label.grid(column=2, row=1)
            article_id_delete_box.grid(column=2, row=2)
            button_delete_btn.grid(column=2, row=3)

            database_lookup_box = tk.Text(root, height=1, width=50)
            placeholder_col_2to4 = tk.Canvas(background="black", width=2, height=height)
            column_4_width = tk.Canvas(width=width / 3, height=1)

            column_4_width.grid(column=4, row=0)
            placeholder_col_2to4.grid(column=3, row=0, rowspan=20)
            database_lookup_label.grid(column=4, row=1)
            database_lookup_box.grid(column=4, row=2)
            database_lookup_btn.grid(column=4, row=3)

            # loop of the window - END!
            root.mainloop()
        finally:
            exit()


if __name__ == '__main__':
    StorageManager()
