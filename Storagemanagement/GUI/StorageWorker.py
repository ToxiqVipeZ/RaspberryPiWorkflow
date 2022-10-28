import tkinter as tk
from tkinter import ttk
from threading import Thread
import time
import sys
from Backend.CassetteScanner import CassetteScanner
from Backend.StorageWorkerBackend import StorageWorkerBackend


class StorageWorker:
    Backend = StorageWorkerBackend()
    CScanner = CassetteScanner()
    data = Backend.get_article_to_pack()

    if data == (0, 0):
        data = 0
        data_split = 0
    else:
        data_split = data[1]

    state = 9
    part_id = 0
    part_amount = 0
    cassette_scanned = 0
    cassette_queue = []
    packed_queue = []
    not_in_cassettes = []
    """
        x                = article number position
        data_split[x][0] = part IDs
        data_split[x][1] = part amounts
        data_split[x][2] = in cassette -> None if not in cassette
    """

    def exec_after_scan(self):
        while self.CScanner.get_triggered_cassette() == 0:
            time.sleep(1)

        if self.CScanner.get_triggered_cassette() != 0:
            self.cassette_scanned = self.CScanner.get_triggered_cassette()
            for x in range(0, len(self.data_split)):
                if self.cassette_scanned == self.data_split[x][2]:
                    print("eintrag gefunden für x: " + str(x))
                    print(self.data_split[x][0])
                    self.part_id = self.data_split[x][0]
                    self.part_amount = self.data_split[x][1]
                    self.state = self.Backend.min_amount_check(self.cassette_scanned, self.part_amount)
                    print(self.state)
                    if self.state == 0:
                        print("X1")
                        self.Backend.cassette_out_triggered(self.cassette_scanned, self.part_id, self.part_amount)

                    elif self.state == 1:
                        print("X2")
                        self.Backend.set_feedback_message("Mindestbestand für \"" + self.part_id + "\" erreicht")
                        self.Backend.cassette_out_triggered(self.cassette_scanned, self.part_id, self.part_amount)

                    elif self.state == 2:
                        print("X3")
                        self.Backend.set_feedback_message("Bestand für \"" + self.part_id +
                                            "\" negativ!\nEs liegt ein Fehler in der Datenhaltung vor.\n"
                                            "Bitte Korrigieren / Inventur durchführen")
                        self.Backend.cassette_out_triggered(self.cassette_scanned, self.part_id, self.part_amount)

            self.CScanner.set_triggered_cassette(0)
            self.cassette_scanned = 0

            time.sleep(1)
            self.exec_after_scan()

    def fill_packed_queue(self, part_id):
        self.packed_queue.append(part_id)
        tree3.insert("", tk.END, values=part_id)
        tree3.update()
        #print("0 2 : " + str(self.data_split[3]) + " len:" + str(len(self.data_split[0][2])))
        #print("1 2 : " + str(self.data_split) + " len:" + str(len(self.data_split)))
        print("cassette_queue: " + str(self.cassette_queue))
        print("packed_queue: " + str(self.packed_queue))
        if self.cassette_queue == self.packed_queue:
            done_btn.configure(state="normal")
            for x in range(0, len(self.data_split)):
                if self.data_split[x][2] == "-":
                    self.not_in_cassettes.append(self.data_split[x])

    def queues_reset(self):
        self.packed_queue = []
        self.cassette_queue = []

    def treeview_creator(self):
        """
        Creates the different tables in the root-frame, as a treeview item.
        """
        self.data = self.Backend.get_article_to_pack()

        # The first table, including the articles, waiting to be packed

        columns = "article_id"
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=("Tekton Pro", 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading",
                        font=("Tekton Pro", 11, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview",
                     [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        tree = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview", height=20)

        tree.column("article_id", anchor="center")
        tree.heading("article_id", text="Artikel-IDs:")
        tree.grid(columnspan=1, rowspan=1, column=0, row=1)

        # The seconds table, including the parts that have to be packed

        columns = ("article_id", "part_ids", "part_amounts", "in_cassette")
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=("Tekton Pro", 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading",
                        font=("Tekton Pro", 11, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        tree2 = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview", height=20)

        tree2.column("article_id", anchor="center")
        tree2.column("part_ids", anchor="center")
        tree2.column("part_amounts", anchor="center")
        tree2.column("in_cassette", anchor="center")

        tree2.heading("article_id", text="Artikel ID:")
        tree2.heading("part_ids", text="Teile-ID:")
        tree2.heading("part_amounts", text="Menge:")
        tree2.heading("in_cassette", text="in Schote:")

        tree2.grid(column=1, row=1, rowspan=1, columnspan=1)

        # The third table, showing already packed items

        columns = "part_ids"
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=("Tekton Pro", 10))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading",
                        font=("Tekton Pro", 11, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        global tree3
        tree3 = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview", height=20)

        tree3.column("part_ids", anchor="center")

        tree3.heading("part_ids", text="Gepackt: ")

        tree3.grid(column=2, row=1, rowspan=1, columnspan=1)

        print(self.data)

        # check if data exists:
        if self.data is not None and self.data != 0 and self.data != (0, 0):
            # check if table1(tree1) data exists:
            if self.data[0] is not None and self.data[0] != 0:
                articles_to_pack = self.data[0]
                if articles_to_pack != 0:
                    for x in range(0, len(articles_to_pack)):
                        tree.insert("", tk.END, values=(articles_to_pack[x][2]))
            # check if table2(tree2) data exists:
            if self.data[1] is not None and self.data[1] != 0:
                article_id = self.data_split[0]
                if article_id != 0:
                    tree2.insert("", 0, values=article_id)
                    print("self.datasplit: \n" + str(self.data_split))
                    print("self.datasplit[1]: \n" + str(self.data_split[1]))
                    print("len datasplit[1]: " + str(len(self.data_split[1])))
                    print("len datasplit: " + str(len(self.data_split)))
                    for x in range(1, len(self.data_split)):
                        print("x: " + str(x))
                        tree2.insert("", tk.END, values=(" ",
                                                         self.data_split[x][0],
                                                         self.data_split[x][1],
                                                         self.data_split[x][2]))
            if self.data_split[1][0] is not None:
                for x in range(1, len(self.data_split)):
                    if self.data_split[x][2] != "-":
                        self.cassette_queue.append(self.data_split[x][0])

            print(self.cassette_queue)

            # The fourth table, showing parts in minimum or under minimum amounts

            tree4_label = tk.Label(text="Bestandswarnungen: ", font=("Tekton Pro", 14, 'bold'), background="#489df7")
            tree4_label.grid(column=1, row=2, rowspan=1, columnspan=1)

            columns = ("part_id", "amount", "min", "in_cassette")
            style = ttk.Style()
            style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                            font=("Tekton Pro", 10))  # Modify the font of the body
            style.configure("mystyle.Treeview.Heading",
                            font=("Tekton Pro", 11, 'bold'))  # Modify the font of the headings
            style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

            tree4 = ttk.Treeview(root, columns=columns, show="headings", style="mystyle.Treeview", height=10)

            tree4.column("part_id", anchor="center")
            tree4.column("amount", anchor="center")
            tree4.column("min", anchor="center")
            tree4.column("in_cassette", anchor="center")

            tree4.heading("part_id", text="Teilenummer:")
            tree4.heading("amount", text="Menge:")
            tree4.heading("min", text="Minimum:")
            tree4.heading("in_cassette", text="in Schote:")

            tree4.grid(column=1, row=3, rowspan=1, columnspan=1)

            stock_data = self.Backend.stock_data()

            print("stock_data : " + str(stock_data))

            for x in range(0, len(stock_data)):
                tree4.insert("", tk.END, values=(stock_data[x][0],
                                                 stock_data[x][1],
                                                 stock_data[x][2],
                                                 stock_data[x][3]))

            root.update()

        else:
            self.feedback_label("Es sind keine Daten in der Datenbank!", 1, 1)

    def feedback_label(self, message, col, row):
        message_label = tk.Label(root, fg="white",
                                 text=message,
                                 background="#489df7",
                                 font=("Tekton Pro", 14),
                                 width=50)
        message_label.grid(column=col, row=row, rowspan=3, columnspan=1)
        root.update()
        self.Backend.delayed_destroyer(message_label, 2)

    def feedback_popup(self, message):
        popup = tk.Toplevel(background="#489df7")
        popup.title("Alert")

        placeholder = tk.Label(popup, text="", height=2, background="#489df7")
        placeholder.pack()

        label = tk.Label(popup, text=message, background="#489df7", font=("Tekton Pro", 12))
        label.pack()

        placeholder2 = tk.Label(popup, text="", height=1, background="#489df7")
        placeholder2.pack()

        # Testbutton definition
        button1_text = tk.StringVar(popup)
        button1_text.set("Verstanden")
        button1_btn = tk.Button(popup, textvariable=button1_text,
                                command=lambda: (popup.destroy(), popup.quit()),
                                width=10, height=5, background="green")
        button1_btn.pack()
        popup.mainloop()

    def feedback_check(self):
        if self.Backend.feedback_message != "None":
            self.feedback_popup(self.Backend.feedback_message)

    def empty_tables(self):
        print("empty tables called")
        print("self.data:")
        print(self.data)
        while self.data == 0:
            self.data = self.Backend.get_article_to_pack()
            root.update()
            print("heh")
            if self.data != 0:
                self.treeview_creator()
                root.update()
                print("heh")
        if self.data != 0:
            self.treeview_creator()
            root.update()
            print("heh")

    def check_state(self):
        print(self.state)
        print(sys.getrecursionlimit())

        if self.state != 9:
            self.fill_packed_queue(self.part_id)
            self.part_id = 0
            self.part_amount = 0
            self.state = 9

        root.update()
        root.after(1, self.check_state)


    def main(self):
        sys.setrecursionlimit(1000000)
        try:
            global root
            root = tk.Tk()

            # window size:
            width, height = root.winfo_screenwidth(), root.winfo_screenheight()
            root.geometry("%dx%d+0+0" % (width, height))
            root.configure(background="#489df7")

            # background:
            canvas = tk.Canvas(root, width=width, height=height, background="#489df7", highlightthickness=0)
            canvas.config(borderwidth=0)
            # window grid:
            canvas.grid(columnspan=6, rowspan=6)
            #self.treeview_creator()

            # done button definition
            global done_btn
            done_button_text = tk.StringVar()
            done_button_text.set("Fertig")
            done_btn = tk.Button(root, textvariable=done_button_text,
                                 command=lambda: (done_btn.configure(state="disabled"),
                                                  self.Backend.packing_completed(self.data[0][0][2],
                                                                                 self.not_in_cassettes),
                                                  self.feedback_check(),
                                                  self.queues_reset(),
                                                  self.empty_tables()),
                                 width=10, height=5, background="green", state="disabled")
            done_btn.grid(column=3, row=1, rowspan=1)

            reset_button_text = tk.StringVar()
            reset_button_text.set("Aktualisieren")
            reset_btn = tk.Button(root, textvariable=reset_button_text,
                                 command=lambda: (self.queues_reset(),
                                                  self.empty_tables()),
                                 width=10, height=5, background="yellow")
            reset_btn.grid(column=3, row=2, rowspan=1)

            # Testbutton definition
            button1_text = tk.StringVar()
            button1_text.set("Schote 1\nEntnahme")
            button1_btn = tk.Button(root, textvariable=button1_text,
                                    command=lambda: (self.CScanner.set_triggered_cassette(1)),
                                    width=10, height=5, background="green")
            button1_btn.grid(column=3, row=3, rowspan=1)

            # Testbutton definition
            # button2_text = tk.StringVar()
            # button2_text.set("Schote 1\nZugabe")
            # button2_btn = tk.Button(root, textvariable=button2_text,
            #                         command=lambda: (),
            #                         width=10, height=5, background="red")
            # button2_btn.grid(column=2, row=1, rowspan=5)

            root.after(1000, Thread(target=self.exec_after_scan).start())

            root.after(1000, self.empty_tables())

            root.after(1000, self.check_state)
            # root.after(1000, self.exec_after_scan)

            root.mainloop()
        finally:
            self.Backend.send_disconnect()

if __name__ == '__main__':
    StorageWorker().main()
