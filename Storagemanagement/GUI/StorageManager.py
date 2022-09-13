import tkinter as tk
from tkinter import ttk

from Storagemanagement.Backend.StorageManagerBackend import StorageManagerBackend


class StorageManager:
    Backend = StorageManagerBackend()

    def __init__(self):
        self.main()

    def show_articles(self):
        popup3 = tk.Toplevel()
        # window-size:
        popup3.geometry("%dx%d+0+0" % (225, 500))
        popup3.configure(background="#489df7", borderwidth=10)

        # background & grid size:
        canvas = tk.Canvas(popup3, width=200, height=500, background="#489df7")
        canvas.config(borderwidth=0, highlightthickness=0)
        canvas.grid(columnspan=1, rowspan=1)

        # table:
        columns = ("article_id")
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=0,
                        font=("Tekton Pro", 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading",
                        font=("Tekton Pro", 11, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        tree = ttk.Treeview(popup3, columns=columns, show="headings", style="mystyle.Treeview", height=20)

        tree.column("article_id", anchor="center")
        tree.heading("article_id", text="Artikel-IDs:")

        relations = self.Backend.get_article_relations()

        for x in range(0, len(relations)):
            tree.insert("", tk.END, values=(relations[x]))

        tree.grid(columnspan=1, rowspan=1, column=0, row=0)

    def warehouse_table(self, popup2):
        # table:
        columns = ("part_id", "part_amount", "part_min_amount", "in_cassette")
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=1, bd=0,
                        font=("Tekton Pro", 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading",
                        font=("Tekton Pro", 11, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        tree = ttk.Treeview(popup2, columns=columns, show="headings", style="mystyle.Treeview", height=20)

        tree.column("part_id", anchor="center")
        tree.column("part_amount", anchor="center")
        tree.column("part_min_amount", anchor="center")
        tree.column("in_cassette", anchor="center")

        tree.heading("part_id", text="Teilenummer:")
        tree.heading("part_amount", text="Menge:")
        tree.heading("part_min_amount", text="Minimum:")
        tree.heading("in_cassette", text="in Schoten:")
        parts = self.Backend.get_stored_parts()

        for x in range(0, len(parts)):
            tree.insert("", tk.END, values=(parts[x][0], parts[x][1], parts[x][2]))

        tree.grid(columnspan=2, rowspan=5, column=3, row=0)

    def config_warehouse(self):
        popup2 = tk.Toplevel()
        # window-size:
        width = 1050
        height = 475
        popup2.geometry("%dx%d+0+0" % (width, height))
        popup2.configure(background="#489df7", borderwidth=10)

        # background & grid size:
        canvas = tk.Canvas(popup2, width=width-100, height=height, background="#489df7")
        canvas.config(borderwidth=0, highlightthickness=0)
        canvas.grid(columnspan=5, rowspan=5)

        # first table-render:
        self.warehouse_table(popup2)

        # labels:
        add_part_label = tk.Label(popup2, fg="white", text="Teilenummer: ",
                                  background="#489df7",
                                  font=("Tekton Pro", 12))
        add_part_amount_label = tk.Label(popup2, fg="white", text="Menge: ",
                                         background="#489df7",
                                         font=("Tekton Pro", 12))

        add_min_amount_label = tk.Label(popup2, fg="white", text="Min-Menge: ",
                                         background="#489df7",
                                         font=("Tekton Pro", 12))

        # textbox's:
        part_number_box = tk.Entry(popup2, width=20, font=("Tekton Pro", 12))
        part_amount_box = tk.Entry(popup2, width=3, font=("Tekton Pro", 12))
        part_min_amount_box = tk.Entry(popup2, width=3, font=("Tekton Pro", 12))

        # buttons:
        add_part_btn = tk.Button(popup2,
                                 text="Speichern",
                                 background="#489df7",
                                 command=lambda: (
                                     self.Backend.save_part_to_store(part_number_box.get(),
                                                                     part_amount_box.get(),
                                                                     part_min_amount_box.get()
                                                                     ),
                                     self.feedback_label(popup2, self.Backend.feedback_message, 3, 4),
                                     self.warehouse_table(popup2),
                                     popup2.update()
                                 ),
                                 font=("Tekton Pro", 10))

        delete_part_btn = tk.Button(popup2, text="Löschen",
                                    background="red",
                                    command=lambda: (
                                        self.Backend.delete_part_from_store(part_number_box.get(),
                                                                            part_amount_box.get()),
                                        self.feedback_label(popup2, self.Backend.feedback_message, 3, 4),
                                        self.warehouse_table(popup2),
                                        popup2.update()
                                    ),
                                    font=("Tekton Pro", 10))

        placeholder_mid = tk.Canvas(popup2, background="#489df7", width=10, highlightthickness=0)
        # alignment:
        add_part_label.grid(columnspan=2, rowspan=1, column=0, row=0)
        part_number_box.grid(columnspan=2, rowspan=1, column=0, row=1)
        add_part_amount_label.grid(columnspan=1, rowspan=1, column=0, row=2)
        add_min_amount_label.grid(columnspan=1, rowspan=1, column=1, row=2)
        part_amount_box.grid(columnspan=1, rowspan=1, column=0, row=3)
        part_min_amount_box.grid(columnspan=1, rowspan=1, column=1, row=3)
        add_part_btn.grid(columnspan=1, rowspan=1, column=0, row=4)
        delete_part_btn.grid(columnspan=1, rowspan=1, column=1, row=4)
        placeholder_mid.grid(columnspan=1, rowspan=5, column=2, row=0)

        # show_parts_label = tk.Label(popup2, fg="white", text="Existierende Teileliste ausgeben: ")
        # show_parts_btn = tk.Entry(popup2)

        popup2.mainloop()

    def config_cassettes(self):
        popup = tk.Toplevel()
        Backend = StorageManagerBackend()

        popup.geometry("%dx%d+0+0" % (1700, 600))
        popup.configure(background="#489df7", highlightthickness=0)

        # background:
        canvas = tk.Canvas(popup, width=1600, height=600, background="#489df7")
        canvas.config(borderwidth=0, highlightthickness=0)
        # window grid:
        canvas.grid(columnspan=9, rowspan=4)

        cassette1_label = tk.Label(popup, fg="white", text="Schote 1:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette1 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(1)), width=20)
        cassette1_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(1)), width=3)

        cassette2_label = tk.Label(popup, fg="white", text="Schote 2:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette2 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(2)), width=20)
        cassette2_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(2)), width=3)

        cassette3_label = tk.Label(popup, fg="white", text="Schote 3:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette3 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(3)), width=20)
        cassette3_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(3)), width=3)

        cassette4_label = tk.Label(popup, fg="white", text="Schote 4:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette4 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(4)), width=20)
        cassette4_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(4)), width=3)

        cassette5_label = tk.Label(popup, fg="white", text="Schote 5:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette5 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(5)), width=20)
        cassette5_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(5)), width=3)

        cassette6_label = tk.Label(popup, fg="white", text="Schote 6:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette6 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(6)), width=20)
        cassette6_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(6)), width=3)

        cassette7_label = tk.Label(popup, fg="white", text="Schote 7:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette7 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(7)), width=20)
        cassette7_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(7)), width=3)

        cassette8_label = tk.Label(popup, fg="white", text="Schote 8:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette8 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(8)), width=20)
        cassette8_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(8)), width=3)

        cassette9_label = tk.Label(popup, fg="white", text="Schote 9:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette9 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(9)), width=20)
        cassette9_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(9)), width=3)

        cassette10_label = tk.Label(popup, fg="white", text="Schote 10:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette10 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(10)), width=20)
        cassette10_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(10)), width=3)

        cassette11_label = tk.Label(popup, fg="white", text="Schote 11:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette11 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(11)), width=20)
        cassette11_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(11)), width=3)

        cassette12_label = tk.Label(popup, fg="white", text="Schote 12:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette12 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(12)), width=20)
        cassette12_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(12)), width=3)

        cassette13_label = tk.Label(popup, fg="white", text="Schote 13:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette13 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(13)), width=20)
        cassette13_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(13)), width=3)

        cassette14_label = tk.Label(popup, fg="white", text="Schote 14:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette14 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(14)), width=20)
        cassette14_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(14)), width=3)

        cassette15_label = tk.Label(popup, fg="white", text="Schote 15:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette15 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(15)), width=20)
        cassette15_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(15)), width=3)

        cassette16_label = tk.Label(popup, fg="white", text="Schote 16:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette16 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(16)), width=20)
        cassette16_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(16)), width=3)

        cassette17_label = tk.Label(popup, fg="white", text="Schote 17:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette17 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(17)), width=20)
        cassette17_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(17)), width=3)

        cassette18_label = tk.Label(popup, fg="white", text="Schote 18:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette18 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(18)), width=20)
        cassette18_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(18)), width=3)

        cassette19_label = tk.Label(popup, fg="white", text="Schote 19:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette19 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(19)), width=20)
        cassette19_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(19)), width=3)

        cassette20_label = tk.Label(popup, fg="white", text="Schote 20:", background="#489df7", font=("Tekton Pro", 10), width=20)
        cassette20 = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_cassette_contains(20)), width=20)
        cassette20_amount = tk.Entry(popup, textvariable=tk.StringVar(popup, value=Backend.get_contains_amount(20)), width=3)

        # when the save button is pressed, take_input gets called
        button_save_btn = tk.Button(popup, text="Speichern",
                                    command=lambda: (
                                        Backend.save_cassette_contains(1, cassette1.get(), cassette1_amount.get()),
                                        Backend.save_cassette_contains(2, cassette2.get(), cassette2_amount.get()),
                                        Backend.save_cassette_contains(3, cassette3.get(), cassette3_amount.get()),
                                        Backend.save_cassette_contains(4, cassette4.get(), cassette4_amount.get()),
                                        Backend.save_cassette_contains(5, cassette5.get(), cassette5_amount.get()),
                                        Backend.save_cassette_contains(6, cassette6.get(), cassette6_amount.get()),
                                        Backend.save_cassette_contains(7, cassette7.get(), cassette7_amount.get()),
                                        Backend.save_cassette_contains(8, cassette8.get(), cassette8_amount.get()),
                                        Backend.save_cassette_contains(9, cassette9.get(), cassette9_amount.get()),
                                        Backend.save_cassette_contains(10, cassette10.get(), cassette10_amount.get()),
                                        Backend.save_cassette_contains(11, cassette11.get(), cassette11_amount.get()),
                                        Backend.save_cassette_contains(12, cassette12.get(), cassette12_amount.get()),
                                        Backend.save_cassette_contains(13, cassette13.get(), cassette13_amount.get()),
                                        Backend.save_cassette_contains(14, cassette14.get(), cassette14_amount.get()),
                                        Backend.save_cassette_contains(15, cassette15.get(), cassette15_amount.get()),
                                        Backend.save_cassette_contains(16, cassette16.get(), cassette16_amount.get()),
                                        Backend.save_cassette_contains(17, cassette17.get(), cassette17_amount.get()),
                                        Backend.save_cassette_contains(18, cassette18.get(), cassette18_amount.get()),
                                        Backend.save_cassette_contains(19, cassette19.get(), cassette19_amount.get()),
                                        Backend.save_cassette_contains(20, cassette20.get(), cassette20_amount.get()),
                                        popup.update()
                                    ),
                                    width=8, height=1, background="#2118f5", fg="white", font=("Tekton Pro", 14))

        cassette1_label.grid(column=0, row=0, columnspan=1, rowspan=1)
        cassette1.grid(column=0, row=0, columnspan=1, rowspan=2)
        cassette1_amount.grid(column=0, row=0, columnspan=2, rowspan=2)

        cassette2_label.grid(column=1, row=0, columnspan=1, rowspan=1)
        cassette2.grid(column=1, row=0, columnspan=1, rowspan=2)
        cassette2_amount.grid(column=1, row=0, columnspan=2, rowspan=2)

        cassette3_label.grid(column=2, row=0, columnspan=1, rowspan=1)
        cassette3.grid(column=2, row=0, columnspan=1, rowspan=2)
        cassette3_amount.grid(column=2, row=0, columnspan=2, rowspan=2)

        cassette4_label.grid(column=3, row=0, columnspan=1, rowspan=1)
        cassette4.grid(column=3, row=0, columnspan=1, rowspan=2)
        cassette4_amount.grid(column=3, row=0, columnspan=2, rowspan=2)

        cassette5_label.grid(column=4, row=0, columnspan=1, rowspan=1)
        cassette5.grid(column=4, row=0, columnspan=1, rowspan=2)
        cassette5_amount.grid(column=4, row=0, columnspan=2, rowspan=2)

        cassette6_label.grid(column=5, row=0, columnspan=1, rowspan=1)
        cassette6.grid(column=5, row=0, columnspan=1, rowspan=2)
        cassette6_amount.grid(column=5, row=0, columnspan=2, rowspan=2)

        cassette7_label.grid(column=6, row=0, columnspan=1, rowspan=1)
        cassette7.grid(column=6, row=0, columnspan=1, rowspan=2)
        cassette7_amount.grid(column=6, row=0, columnspan=2, rowspan=2)

        cassette8_label.grid(column=7, row=0, columnspan=1, rowspan=1)
        cassette8.grid(column=7, row=0, columnspan=1, rowspan=2)
        cassette8_amount.grid(column=8, row=0, columnspan=1, rowspan=2)

        cassette9_label.grid(column=0, row=1, columnspan=1, rowspan=1)
        cassette9.grid(column=0, row=1, columnspan=1, rowspan=2)
        cassette9_amount.grid(column=0, row=1, columnspan=2, rowspan=2)

        cassette10_label.grid(column=1, row=1, columnspan=1, rowspan=1)
        cassette10.grid(column=1, row=1, columnspan=1, rowspan=2)
        cassette10_amount.grid(column=1, row=1, columnspan=2, rowspan=2)

        cassette11_label.grid(column=2, row=1, columnspan=1, rowspan=1)
        cassette11.grid(column=2, row=1, columnspan=1, rowspan=2)
        cassette11_amount.grid(column=2, row=1, columnspan=2, rowspan=2)

        cassette12_label.grid(column=3, row=1, columnspan=1, rowspan=1)
        cassette12.grid(column=3, row=1, columnspan=1, rowspan=2)
        cassette12_amount.grid(column=3, row=1, columnspan=2, rowspan=2)

        cassette13_label.grid(column=4, row=1, columnspan=1, rowspan=1)
        cassette13.grid(column=4, row=1, columnspan=1, rowspan=2)
        cassette13_amount.grid(column=4, row=1, columnspan=2, rowspan=2)

        cassette14_label.grid(column=5, row=1, columnspan=1, rowspan=1)
        cassette14.grid(column=5, row=1, columnspan=1, rowspan=2)
        cassette14_amount.grid(column=5, row=1, columnspan=2, rowspan=2)

        cassette15_label.grid(column=6, row=1, columnspan=1, rowspan=1)
        cassette15.grid(column=6, row=1, columnspan=1, rowspan=2)
        cassette15_amount.grid(column=6, row=1, columnspan=2, rowspan=2)

        cassette16_label.grid(column=0, row=2, columnspan=1, rowspan=1)
        cassette16.grid(column=0, row=2, columnspan=1, rowspan=2)
        cassette16_amount.grid(column=0, row=2, columnspan=2, rowspan=2)

        cassette17_label.grid(column=1, row=2, columnspan=1, rowspan=1)
        cassette17.grid(column=1, row=2, columnspan=1, rowspan=2)
        cassette17_amount.grid(column=1, row=2, columnspan=2, rowspan=2)

        cassette18_label.grid(column=2, row=2, columnspan=1, rowspan=1)
        cassette18.grid(column=2, row=2, columnspan=1, rowspan=2)
        cassette18_amount.grid(column=2, row=2, columnspan=2, rowspan=2)

        cassette19_label.grid(column=3, row=2, columnspan=1, rowspan=1)
        cassette19.grid(column=3, row=2, columnspan=1, rowspan=2)
        cassette19_amount.grid(column=3, row=2, columnspan=2, rowspan=2)

        cassette20_label.grid(column=4, row=2, columnspan=1, rowspan=1)
        cassette20.grid(column=4, row=2, columnspan=1, rowspan=2)
        cassette20_amount.grid(column=4, row=2, columnspan=2, rowspan=2)

        button_save_btn.grid(column=7, row=2, columnspan=1, rowspan=2)

        popup.mainloop()

    def treeview_creator(self, root, database_lookup_box):
        columns = ("article_id", "part_ids", "part_amounts")

        data = self.Backend.lookup_article_parts_relations(database_lookup_box)

        if data is not None:
            style = ttk.Style()
            style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                            font=("Tekton Pro", 10))  # Modify the font of the body
            style.configure("mystyle.Treeview.Heading",
                            font=("Tekton Pro", 11, 'bold'))  # Modify the font of the headings
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
                tree.insert("", tk.END, values=(" ", splitted_parts[x], split_part_amounts[x]))

            tree.insert("", 0, values=article_id)
            tree.grid(column=5, row=4, rowspan=2, columnspan=1)
            root.update()

    def feedback_label(self, root, message, col, row):
        message_label = tk.Label(root, fg="white",
                                 text=message,
                                 background="#489df7",
                                 font=("Tekton Pro", 10),
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
            root.configure(background="#489df7")
            root.state("zoomed")
            # background:
            canvas = tk.Canvas(root, width=width, height=height, background="#489df7", highlightthickness=0)
            canvas.config(borderwidth=0)
            # window grid:
            canvas.grid(columnspan=7, rowspan=10)

            # label definition:
            article_id_box_label = tk.Label(root, fg="white",
                                            text="Artikel-ID:",
                                            background="#489df7",
                                            font=("Tekton Pro", 15))
            part_numbers_box_label = tk.Label(root, fg="white",
                                              text="Teilenummern x Menge: \n(Bsp.: 015231x7)",
                                              background="#489df7",
                                              font=("Tekton Pro", 15))
            article_id_delete_label = tk.Label(root, fg="white",
                                               text="Artikel-ID löschen:",
                                               background="#489df7",
                                               font=("Tekton Pro", 15))
            database_lookup_label = tk.Label(root, fg="white",
                                             text="Artikel-ID suchen:",
                                             background="#489df7",
                                             font=("Tekton Pro", 15))
            configure_cassettes_label = tk.Label(root, fg="white",
                                                 text="Schoten\nVerwaltung: ",
                                                 background="#489df7",
                                                 font=("Tekton Pro", 15),
                                                 pady=20)
            warehouse_label = tk.Label(root, fg="white",
                                       text="Lagerverwaltung: ",
                                       background="#489df7",
                                       font=("Tekton Pro", 15))

            # when the save button is pressed, take_input gets called
            button_save_btn = tk.Button(root, text="Speichern",
                                        command=lambda: (
                                            self.Backend.save_article_parts_relations(
                                                article_id_box,
                                                part_numbers_box
                                            ),
                                            self.feedback_label(root, self.Backend.feedback_message, 3, 6)
                                        ),
                                        width=8, height=1, background="#2118f5", fg="white",
                                        font=("Tekton Pro", 14))

            button_delete_btn = tk.Button(root, text="Löschen",
                                          command=lambda: (
                                              self.Backend.delete_article_parts_relations(
                                                  article_id_delete_box
                                              ),
                                              self.feedback_label(root, self.Backend.feedback_message, 3, 6)
                                          ),
                                          width=8, height=1, background="#2118f5", fg="white",
                                          font=("Tekton Pro", 14))

            database_lookup_btn = tk.Button(root, text="Ausgeben",
                                            command=lambda: (
                                                self.treeview_creator(root, database_lookup_box),
                                                self.feedback_label(root, self.Backend.feedback_message, 3, 6)
                                            ),
                                            width=8, height=1, background="#2118f5", fg="white",
                                            font=("Tekton Pro", 14))

            configure_cassettes_btn = tk.Button(root, text="Konfig.",
                                                command=lambda: (
                                                    self.config_cassettes()
                                                ),
                                                width=8, height=1, background="#2118f5", fg="white",
                                                font=("Tekton Pro", 14))
            configure_warehouse_btn = tk.Button(root, text="Konfig.",
                                                command=lambda: (
                                                    self.config_warehouse()
                                                ),
                                                width=8, height=1, background="#2118f5", fg="white",
                                                font=("Tekton Pro", 14))
            show_relations_btn = tk.Button(root, text="Angelegte Anzeigen",
                                           command=lambda: (
                                               self.show_articles()
                                           ),
                                           width=16, height=1, background="#2118f5", fg="white",
                                           font=("Tekton Pro", 12))

            # placeholder = tk.Canvas(width=0, height=0)
            # placeholder.grid(column=0, rowspan=10)

            article_id_box = tk.Text(root, height=1, width=50)
            part_numbers_box = tk.Text(root, height=20, width=50)
            column_1_width = tk.Canvas(width=(width / 3) - 20, height=0, borderwidth=0, bg="#489df7")

            column_1_width.grid(column=1, row=10)
            article_id_box_label.grid(column=1, row=1, rowspan=2, columnspan=1)
            article_id_box.grid(column=1, row=2, rowspan=1, columnspan=1)
            part_numbers_box_label.grid(column=1, row=3, rowspan=1, columnspan=1)
            part_numbers_box.grid(column=1, row=4, rowspan=1, columnspan=1)
            button_save_btn.grid(column=1, row=5, rowspan=1, columnspan=1)
            show_relations_btn.grid(column=1, row=6, rowspan=1, columnspan=1)

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
