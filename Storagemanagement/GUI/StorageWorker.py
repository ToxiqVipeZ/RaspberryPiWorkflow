import tkinter as tk
from tkinter import ttk
from threading import Thread
from Storagemanagement.Backend.CassetteScanner import CassetteScanner
from Storagemanagement.Backend.StorageWorkerBackend import StorageWorkerBackend


class StorageWorker:
    Backend = StorageWorkerBackend()
    CScanner = CassetteScanner()
    data = Backend.get_article_to_pack()
    """
        x                = article number position
        data_split[x][0] = part IDs
        data_split[x][1] = part amounts
        data_split[x][2] = in cassette -> None if not in cassette
    """
    data_split = data[1]

    def scanning_cassettes(self):
        scanning_cassettes = self.CScanner.get_triggered_cassette()

    def treeview_creator(self, root):

        if self.data is not None:

            if self.data[0] is not None:
                # articles-to-pack table:
                columns = ("article_id")
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

                articles_to_pack = self.data[0]

                for x in range(0, len(articles_to_pack)):
                    tree.insert("", tk.END, values=(articles_to_pack[x][1]))

                tree.grid(columnspan=1, rowspan=1, column=0, row=0)

            if self.data[1] is not None:
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

                article_id = self.data_split[0]

                # splitted_parts = (data[1].split("\', \'"))
                # splitted_parts[0] = splitted_parts[0][2:]
                # splitted_parts[len(splitted_parts) - 1] = splitted_parts[len(splitted_parts) - 1][:-2]
                #
                # split_part_amounts = (data[2].split("\', \'"))
                # split_part_amounts[0] = split_part_amounts[0][2:]
                # split_part_amounts[len(split_part_amounts) - 1] = split_part_amounts[len(split_part_amounts) - 1][:-2]

                for x in range(1, len(self.data_split[1])+1):
                    print("das ist x: " + str(x))
                    tree2.insert("", tk.END, values=(" ",
                                                     self.data_split[x][0],
                                                     self.data_split[x][1],
                                                     self.data_split[x][2]))

                tree2.insert("", 0, values=article_id)
                tree2.grid(column=1, row=0, rowspan=1, columnspan=1)
                root.update()

        else:
            self.feedback_label(root, "Es sind keine Daten in der Datenbank!", 1, 1)

    def feedback_label(self, root, message, col, row):
        message_label = tk.Label(root, fg="white",
                                 text=message,
                                 background="#489df7",
                                 font=("Tekton Pro", 14),
                                 width=50)
        message_label.grid(column=col, row=row, rowspan=3, columnspan=1)
        root.update()
        self.Backend.delayed_destroyer(message_label, 2)

    def main(self):
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
        self.treeview_creator(root)

        root.after(1000, Thread(target=self.scanning_cassettes).start())

        root.mainloop()


if __name__ == '__main__':
    StorageWorker().main()
