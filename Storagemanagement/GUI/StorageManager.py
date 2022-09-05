import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

from Storagemanagement.Backend.StorageManagerBackend import StorageManagerBackend


class StorageManager:
    Backend = StorageManagerBackend()

    def __init__(self):
        self.main()

    def config_warehouse(self):
        popup2 = tk.Toplevel()
        # window-size:
        popup2.geometry("%dx%d+0+0" % (800, 400))
        popup2.configure(background="grey")

        # background & grid size:
        canvas = tk.Canvas(popup2, width=800, height=400, background="grey")
        canvas.config(borderwidth=0, highlightthickness=0)
        canvas.grid(columnspan=10, rowspan=5)

        # labels:
        add_part_label = tk.Label(popup2, text="Teilenummer: ",
                                  background="grey",
                                  font=("Arial Black", 12))
        add_part_amount_label = tk.Label(popup2, text="Menge: ",
                                         background="grey",
                                         font=("Arial Black", 12))

        # textbox's:
        part_number_box = tk.Entry(popup2, width=20, font=("Arial Black", 12))
        part_amount_box = tk.Entry(popup2, width=3, font=("Arial Black", 12))

        # buttons:
        add_part_btn = tk.Button(popup2, text="hinzufügen",
                                 background="grey",
                                 font=("Arial Black", 10))
        delete_part_btn = tk.Button(popup2, text="löschen",
                                    background="red",
                                    font=("Arial Black", 10))

        # table:
        self.Backend.get_parts_table()

        # alignment:
        add_part_label.grid(columnspan=2, rowspan=1, column=0, row=0)
        part_number_box.grid(columnspan=2, rowspan=1, column=0, row=1)
        add_part_amount_label.grid(columnspan=2, rowspan=1, column=0, row=2)
        part_amount_box.grid(columnspan=2, rowspan=1, column=0, row=3)
        add_part_btn.grid(columnspan=1, rowspan=1, column=0, row=4)
        delete_part_btn.grid(columnspan=1, rowspan=1, column=1, row=4)

        #show_parts_label = tk.Label(popup2, text="Existierende Teileliste ausgeben: ")
        #show_parts_btn = tk.Entry(popup2)

        popup2.mainloop()

    def config_cassettes(self):
        popup = tk.Toplevel()
        Backend = StorageManagerBackend()

        popup.geometry("%dx%d+0+0" % (1700, 600))
        popup.configure(background="grey", highlightthickness=0)

        # background:
        canvas = tk.Canvas(popup, width=1600, height=600, background="grey")
        canvas.config(borderwidth=0, highlightthickness=0)
        # window grid:
        canvas.grid(columnspan=9, rowspan=4)

        box1_label = tk.Label(popup, text="Box1:", background="grey", font=("Arial Black", 10), width=20)
        box1 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(1)), width=20)
        box1_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(1)), width=3)

        box2_label = tk.Label(popup, text="Box2:", background="grey", font=("Arial Black", 10), width=20)
        box2 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(2)), width=20)
        box2_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(2)), width=3)

        box3_label = tk.Label(popup, text="Box3:", background="grey", font=("Arial Black", 10), width=20)
        box3 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(3)), width=20)
        box3_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(3)), width=3)

        box4_label = tk.Label(popup, text="Box4:", background="grey", font=("Arial Black", 10), width=20)
        box4 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(4)), width=20)
        box4_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(4)), width=3)

        box5_label = tk.Label(popup, text="Box5:", background="grey", font=("Arial Black", 10), width=20)
        box5 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(5)), width=20)
        box5_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(5)), width=3)

        box6_label = tk.Label(popup, text="Box6:", background="grey", font=("Arial Black", 10), width=20)
        box6 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(6)), width=20)
        box6_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(6)), width=3)

        box7_label = tk.Label(popup, text="Box7:", background="grey", font=("Arial Black", 10), width=20)
        box7 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(7)), width=20)
        box7_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(7)), width=3)

        box8_label = tk.Label(popup, text="Box8:", background="grey", font=("Arial Black", 10), width=20)
        box8 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(8)), width=20)
        box8_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(8)), width=3)

        box9_label = tk.Label(popup, text="Box9:", background="grey", font=("Arial Black", 10), width=20)
        box9 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(9)), width=20)
        box9_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(9)), width=3)

        box10_label = tk.Label(popup, text="Box10:", background="grey", font=("Arial Black", 10), width=20)
        box10 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(10)), width=20)
        box10_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(10)), width=3)

        box11_label = tk.Label(popup, text="Box11:", background="grey", font=("Arial Black", 10), width=20)
        box11 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(11)), width=20)
        box11_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(11)), width=3)

        box12_label = tk.Label(popup, text="Box12:", background="grey", font=("Arial Black", 10), width=20)
        box12 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(12)), width=20)
        box12_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(12)), width=3)

        box13_label = tk.Label(popup, text="Box13:", background="grey", font=("Arial Black", 10), width=20)
        box13 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(13)), width=20)
        box13_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(13)), width=3)

        box14_label = tk.Label(popup, text="Box14:", background="grey", font=("Arial Black", 10), width=20)
        box14 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(14)), width=20)
        box14_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(14)), width=3)

        box15_label = tk.Label(popup, text="Box15:", background="grey", font=("Arial Black", 10), width=20)
        box15 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(15)), width=20)
        box15_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(15)), width=3)

        box16_label = tk.Label(popup, text="Box16:", background="grey", font=("Arial Black", 10), width=20)
        box16 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(16)), width=20)
        box16_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(16)), width=3)

        box17_label = tk.Label(popup, text="Box17:", background="grey", font=("Arial Black", 10), width=20)
        box17 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(17)), width=20)
        box17_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(17)), width=3)

        box18_label = tk.Label(popup, text="Box18:", background="grey", font=("Arial Black", 10), width=20)
        box18 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(18)), width=20)
        box18_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(18)), width=3)

        box19_label = tk.Label(popup, text="Box19:", background="grey", font=("Arial Black", 10), width=20)
        box19 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(19)), width=20)
        box19_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(19)), width=3)

        box20_label = tk.Label(popup, text="Box20:", background="grey", font=("Arial Black", 10), width=20)
        box20 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(20)), width=20)
        box20_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(20)), width=3)

        # when the save button is pressed, take_input gets called
        button_save_btn = tk.Button(popup, text="Speichern",
                                    command=lambda: (
                                        Backend.save_cassette_contains(1, box1.get(), box1_amount.get()),
                                        Backend.save_cassette_contains(2, box2.get(), box2_amount.get()),
                                        Backend.save_cassette_contains(3, box3.get(), box3_amount.get()),
                                        Backend.save_cassette_contains(4, box4.get(), box4_amount.get()),
                                        Backend.save_cassette_contains(5, box5.get(), box5_amount.get()),
                                        Backend.save_cassette_contains(6, box6.get(), box6_amount.get()),
                                        Backend.save_cassette_contains(7, box7.get(), box7_amount.get()),
                                        Backend.save_cassette_contains(8, box8.get(), box8_amount.get()),
                                        Backend.save_cassette_contains(9, box9.get(), box9_amount.get()),
                                        Backend.save_cassette_contains(10, box10.get(), box10_amount.get()),
                                        Backend.save_cassette_contains(11, box11.get(), box11_amount.get()),
                                        Backend.save_cassette_contains(12, box12.get(), box12_amount.get()),
                                        Backend.save_cassette_contains(13, box13.get(), box13_amount.get()),
                                        Backend.save_cassette_contains(14, box14.get(), box14_amount.get()),
                                        Backend.save_cassette_contains(15, box15.get(), box15_amount.get()),
                                        Backend.save_cassette_contains(16, box16.get(), box16_amount.get()),
                                        Backend.save_cassette_contains(17, box17.get(), box17_amount.get()),
                                        Backend.save_cassette_contains(18, box18.get(), box18_amount.get()),
                                        Backend.save_cassette_contains(19, box19.get(), box19_amount.get()),
                                        Backend.save_cassette_contains(20, box20.get(), box20_amount.get()),
                                        popup.update()
                                    ),
                                    width=8, height=1, background="green", font=("Arial", 14))

        box1_label.grid(column=0, row=0, columnspan=1, rowspan=1)
        box1.grid(column=0, row=0, columnspan=1, rowspan=2)
        box1_amount.grid(column=0, row=0, columnspan=2, rowspan=2)

        box2_label.grid(column=1, row=0, columnspan=1, rowspan=1)
        box2.grid(column=1, row=0, columnspan=1, rowspan=2)
        box2_amount.grid(column=1, row=0, columnspan=2, rowspan=2)

        box3_label.grid(column=2, row=0, columnspan=1, rowspan=1)
        box3.grid(column=2, row=0, columnspan=1, rowspan=2)
        box3_amount.grid(column=2, row=0, columnspan=2, rowspan=2)

        box4_label.grid(column=3, row=0, columnspan=1, rowspan=1)
        box4.grid(column=3, row=0, columnspan=1, rowspan=2)
        box4_amount.grid(column=3, row=0, columnspan=2, rowspan=2)

        box5_label.grid(column=4, row=0, columnspan=1, rowspan=1)
        box5.grid(column=4, row=0, columnspan=1, rowspan=2)
        box5_amount.grid(column=4, row=0, columnspan=2, rowspan=2)

        box6_label.grid(column=5, row=0, columnspan=1, rowspan=1)
        box6.grid(column=5, row=0, columnspan=1, rowspan=2)
        box6_amount.grid(column=5, row=0, columnspan=2, rowspan=2)

        box7_label.grid(column=6, row=0, columnspan=1, rowspan=1)
        box7.grid(column=6, row=0, columnspan=1, rowspan=2)
        box7_amount.grid(column=6, row=0, columnspan=2, rowspan=2)

        box8_label.grid(column=7, row=0, columnspan=1, rowspan=1)
        box8.grid(column=7, row=0, columnspan=1, rowspan=2)
        box8_amount.grid(column=8, row=0, columnspan=1, rowspan=2)

        box9_label.grid(column=0, row=1, columnspan=1, rowspan=1)
        box9.grid(column=0, row=1, columnspan=1, rowspan=2)
        box9_amount.grid(column=0, row=1, columnspan=2, rowspan=2)

        box10_label.grid(column=1, row=1, columnspan=1, rowspan=1)
        box10.grid(column=1, row=1, columnspan=1, rowspan=2)
        box10_amount.grid(column=1, row=1, columnspan=2, rowspan=2)

        box11_label.grid(column=2, row=1, columnspan=1, rowspan=1)
        box11.grid(column=2, row=1, columnspan=1, rowspan=2)
        box11_amount.grid(column=2, row=1, columnspan=2, rowspan=2)

        box12_label.grid(column=3, row=1, columnspan=1, rowspan=1)
        box12.grid(column=3, row=1, columnspan=1, rowspan=2)
        box12_amount.grid(column=3, row=1, columnspan=2, rowspan=2)

        box13_label.grid(column=4, row=1, columnspan=1, rowspan=1)
        box13.grid(column=4, row=1, columnspan=1, rowspan=2)
        box13_amount.grid(column=4, row=1, columnspan=2, rowspan=2)

        box14_label.grid(column=5, row=1, columnspan=1, rowspan=1)
        box14.grid(column=5, row=1, columnspan=1, rowspan=2)
        box14_amount.grid(column=5, row=1, columnspan=2, rowspan=2)

        box15_label.grid(column=6, row=1, columnspan=1, rowspan=1)
        box15.grid(column=6, row=1, columnspan=1, rowspan=2)
        box15_amount.grid(column=6, row=1, columnspan=2, rowspan=2)

        box16_label.grid(column=0, row=2, columnspan=1, rowspan=1)
        box16.grid(column=0, row=2, columnspan=1, rowspan=2)
        box16_amount.grid(column=0, row=2, columnspan=2, rowspan=2)

        box17_label.grid(column=1, row=2, columnspan=1, rowspan=1)
        box17.grid(column=1, row=2, columnspan=1, rowspan=2)
        box17_amount.grid(column=1, row=2, columnspan=2, rowspan=2)

        box18_label.grid(column=2, row=2, columnspan=1, rowspan=1)
        box18.grid(column=2, row=2, columnspan=1, rowspan=2)
        box18_amount.grid(column=2, row=2, columnspan=2, rowspan=2)

        box19_label.grid(column=3, row=2, columnspan=1, rowspan=1)
        box19.grid(column=3, row=2, columnspan=1, rowspan=2)
        box19_amount.grid(column=3, row=2, columnspan=2, rowspan=2)

        box20_label.grid(column=4, row=2, columnspan=1, rowspan=1)
        box20.grid(column=4, row=2, columnspan=1, rowspan=2)
        box20_amount.grid(column=4, row=2, columnspan=2, rowspan=2)

        button_save_btn.grid(column=7, row=2, columnspan=1, rowspan=2)

        popup.mainloop()

    def treeview_creator(self, root, database_lookup_box):
        columns = ("article_id", "part_ids", "part_amounts")

        data = self.Backend.lookup_article_parts_relations(database_lookup_box)

        if data is not None:
            style = ttk.Style()
            style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                            font=("Arial Black", 10))  # Modify the font of the body
            style.configure("mystyle.Treeview.Heading",
                            font=("Arial Black", 11, 'bold'))  # Modify the font of the headings
            style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

            tree = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview", height=20)

            tree.column("article_id", anchor="center")
            tree.column("part_ids", anchor="center")
            tree.column("part_amounts", anchor="center")

            tree.heading("article_id", text="Artikel ID:")
            tree.heading("part_ids", text="Teile-ID:")
            tree.heading("part_amounts", text="Menge:")

            article_id = data[0]

            splitted_parts = (data[1].split("\', \'"))
            splitted_parts[0] = splitted_parts[0][2:]
            splitted_parts[len(splitted_parts) - 1] = splitted_parts[len(splitted_parts) - 1][:-2]

            split_part_amounts = (data[2].split("\', \'"))
            split_part_amounts[0] = split_part_amounts[0][2:]
            split_part_amounts[len(split_part_amounts) - 1] = split_part_amounts[len(split_part_amounts) - 1][:-2]

            for x in range(0, len(split_part_amounts)):
                print(splitted_parts[x], split_part_amounts[x])
                tree.insert("", tk.END, values=(" ", splitted_parts[x], split_part_amounts[x]))

            tree.insert("", 0, values=article_id)
            tree.grid(column=5, row=4, rowspan=3, columnspan=1)
            root.update()

    def feedback_label(self, root, message, col, row):
        message_label = tk.Label(root,
                                 text=message,
                                 background="grey",
                                 font=("Arial Black", 10),
                                 width=50)
        message_label.grid(column=col, row=row, rowspan=3, columnspan=1)
        root.update()
        self.Backend.delayed_destroyer(message_label, 2)

    def main(self):
        try:
            # loop of the window - START!
            root = tk.Tk()

            # window size:
            width, height = root.winfo_screenwidth(), root.winfo_screenheight()
            root.geometry("%dx%d+0+0" % (width, height))
            root.configure(background="grey")
            root.state("zoomed")
            # background:
            canvas = tk.Canvas(root, width=width, height=height, background="grey", highlightthickness=2)
            canvas.config(borderwidth=0)
            # window grid:
            canvas.grid(columnspan=7, rowspan=10)

            # label definition:
            article_id_box_label = tk.Label(root,
                                            text="Artikel-ID:",
                                            background="grey",
                                            font=("Arial Black", 15))
            part_numbers_box_label = tk.Label(root,
                                              text="Teilenummern x Menge: \n(Bsp.: 015231x7)",
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
            configure_cassettes_label = tk.Label(root,
                                                 text="Lager-Kasetten\nVerwaltung: ",
                                                 background="grey",
                                                 font=("Arial Black", 15))
            warehouse_label = tk.Label(root,
                                                 text="Lagerverwaltung: ",
                                                 background="grey",
                                                 font=("Arial Black", 15))

            # when the save button is pressed, take_input gets called
            button_save_btn = tk.Button(root, text="Speichern",
                                        command=lambda: (
                                            self.Backend.save_article_parts_relations(
                                                article_id_box,
                                                part_numbers_box
                                            ),
                                            self.feedback_label(root, self.Backend.feedback_message, 3, 6)
                                        ),
                                        width=8, height=1, background="green", font=("Arial", 14))

            button_delete_btn = tk.Button(root, text="Löschen",
                                          command=lambda: (
                                              self.Backend.delete_article_parts_relations(
                                                  article_id_delete_box
                                              ),
                                              self.feedback_label(root, self.Backend.feedback_message, 3, 6)
                                          ),
                                          width=8, height=1, background="green", font=("Arial", 14))

            database_lookup_btn = tk.Button(root, text="Ausgeben",
                                            command=lambda: (
                                                self.treeview_creator(root, database_lookup_box),
                                                self.feedback_label(root, self.Backend.feedback_message, 3, 6)
                                            ),
                                            width=8, height=1, background="green", font=("Arial", 14))

            configure_cassettes_btn = tk.Button(root, text="Konfig.",
                                                 command=lambda: (
                                                     self.config_cassettes()
                                                 ),
                                                 width=8, height=1, background="green", font=("Arial", 14))
            configure_warehouse_btn = tk.Button(root, text="Konfig.",
                                                command=lambda: (
                                                    self.config_warehouse()
                                                ),
                                                width=8, height=1, background="green", font=("Arial", 14))

            # placeholder = tk.Canvas(width=0, height=0)
            # placeholder.grid(column=0, rowspan=10)

            article_id_box = tk.Text(root, height=1, width=50)
            part_numbers_box = tk.Text(root, height=20, width=50)
            column_1_width = tk.Canvas(width=(width / 3) - 20, height=0, borderwidth=0, bg="grey")

            column_1_width.grid(column=1, row=10)
            article_id_box_label.grid(column=1, row=1, rowspan=2, columnspan=1)
            article_id_box.grid(column=1, row=2, rowspan=1, columnspan=1)
            part_numbers_box_label.grid(column=1, row=3, rowspan=1, columnspan=1)
            part_numbers_box.grid(column=1, row=4, rowspan=1, columnspan=1)
            button_save_btn.grid(column=1, row=5, rowspan=1, columnspan=1)

            # placeholder_col_0to2 = tk.Canvas(background="black", width=1, height=height, highlightcolor="black")
            # placeholder_col_0to2.grid(column=2, row=0, rowspan=10)

            article_id_delete_box = tk.Text(root, height=1, width=50)
            column_3_width = tk.Canvas(width=(width / 3) - 20, height=0)
            # column_3_bottom_border_line = tk.Canvas(width=width / 3, height=1, background="black")

            column_3_width.grid(column=3, row=10)
            article_id_delete_label.grid(column=3, row=1, rowspan=2, columnspan=1)
            article_id_delete_box.grid(column=3, row=2, rowspan=1, columnspan=1)
            button_delete_btn.grid(column=3, row=3, rowspan=1, columnspan=1)
            configure_cassettes_label.grid(column=3, row=3, rowspan=2, columnspan=1)
            configure_cassettes_btn.grid(column=3, row=3, rowspan=4, columnspan=1)
            warehouse_label.grid(column=3, row=4, rowspan=3, columnspan=1)
            configure_warehouse_btn.grid(column=3, row=4, rowspan=5, columnspan=2)
            # column_3_bottom_border_line.grid(column=3, row=7)

            # placeholder_col_2to4 = tk.Canvas(background="black", width=1, height=height)
            # placeholder_col_2to4.grid(column=4, row=0, rowspan=10)

            database_lookup_box = tk.Text(root, height=1, width=50)
            column_5_width = tk.Canvas(width=(width / 3) - 20, height=0)

            column_5_width.grid(column=5, row=10)
            database_lookup_label.grid(column=5, row=1, rowspan=2, columnspan=1)
            database_lookup_box.grid(column=5, row=2, rowspan=1, columnspan=1)
            database_lookup_btn.grid(column=5, row=3, rowspan=1, columnspan=1)

            # placeholder_r = tk.Canvas(width=1, height=height)
            # placeholder_r.grid(column=6, row=0, rowspan=10, columnspan=2)

            # loop of the window - END!
            root.mainloop()
        finally:
            exit()


if __name__ == '__main__':
    StorageManager()
