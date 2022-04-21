import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
import os


class WorkflowPlannerApp:

    def take_input(self, root, text_window, operation):
        text_input = text_window.get("1.0", "end-1c")
        if operation == "save":
            self.database_save(root, text_input)
        if operation == "delete":
            self.database_delete(root, text_input)

    def database_save(self, root, text_input):
        try:
            # connection holds the connection to the database
            # (path\productionDatabase.db)
            connection = sqlite3.connect(
                "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

            # cursor instance:
            c = connection.cursor()

            workflow_procedure_value = text_input.split(";")
            workflow_procedure_value = workflow_procedure_value[:1]
            workflow_procedure_value = ";".join([str(item) for item in workflow_procedure_value])

            stations_value = text_input.split(";")
            stations_value = stations_value[1:]
            stations_value = ";".join([str(item) for item in stations_value])

            print(workflow_procedure_value)
            print(stations_value)

            # workflow_procedure_value = procedure number (examples: 001, 002, 003)
            # stations_value = station number (multiple: [01;02;05, 07;02;01;05,03 ...])
            c.execute("INSERT INTO workflow_planner_table VALUES (?, ?)", (workflow_procedure_value, stations_value))

            success_text = "Daten erfolgreich in Datenbank gespeichert!"
            text_label = tk.Label(root, text=success_text)
            text_label.config(font=("Courier", 14))
            text_label.pack()
            text_label.update()
            text_label.after(2000, text_label.destroy())

            # committing the created table:
            connection.commit()

            # closing the connection
            connection.close()

        except sqlite3.IntegrityError:
            error_text = "Fehlerhaften eingabe oder Verfahren bereits angelegt"
            text_label = tk.Label(root, text=error_text)
            text_label.config(font=("Courier", 14))
            text_label.pack()
            text_label.update()
            root.after(2000, text_label.destroy())

    def database_delete(self, root, text_input):
        # connection holds the connection to the database
        # (path\productionDatabase.db)
        connection = sqlite3.connect(
            "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

        # cursor instance:
        c = connection.cursor()
        print(text_input)
        c.execute("DELETE FROM workflow_planner_table WHERE workflow_procedure = (?)", (text_input,))

        success_text = "Daten erfolgreich aus Datenbank gelöscht!"
        text_label = tk.Label(root, text=success_text)
        text_label.config(font=("Courier", 14))
        text_label.pack()
        text_label.update()
        text_label.after(2000, text_label.destroy())

        # committing the created table:
        connection.commit()

        # closing the connection
        connection.close()

    def main(self):
        """
        the main window, only showing and waiting for an RFID-chip to get read
        """
        # loop of the window - START
        root = tk.Tk()

        width, height = root.winfo_screenwidth(), root.winfo_screenheight()

        # window size
        #canvas_root = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        # window grid
        #canvas_root.grid(columnspan=3, rowspan=3)

        text_save_window = tk.Text(root, height=10, width=40)
        text_label = tk.Label(root, text="Form: \"Verfahren;Fertigung;Montage;Versand;...\""
                                         "\n Beispiel: 001;01;02;05;...")
        text_label.config(font=("Courier", 14))
        text_label.pack()
        text_save_window.pack()

        root.geometry("%dx%d+0+0" % (width, height))

        # button_save definition
        button_save_text = tk.StringVar()
        button_save_text.set("Save")
        button_save_btn = tk.Button(root, textvariable=button_save_text,
                                   command=lambda: (self.take_input(root, text_save_window, "save")),
                                   width=10, height=5, background="green")
        #buttonTest_btn.grid(column=0, row=0)
        button_save_btn.pack()

        # spaceholder
        spaceholder = tk.Label(root, width=10, height=10)
        spaceholder.pack()

        text_delete_window = tk.Text(root, height=5, width=40)
        text_label = tk.Label(root, text="Eintrag entfernen: Verfahren"
                                         "\n Beispiel: 001")
        text_label.config(font=("Courier", 14))
        text_label.pack()
        text_delete_window.pack()

        # button_save definition
        button_delete_text = tk.StringVar()
        button_delete_text.set("Delete")
        button_delete_btn = tk.Button(root, textvariable=button_delete_text,
                                    command=lambda: (self.take_input(root, text_delete_window, "delete")),
                                    width=10, height=5, background="green")
        # buttonTest_btn.grid(column=0, row=0)
        button_delete_btn.pack()

        # loop of the window - END!
        root.mainloop()


WorkflowPlannerApp().main()
