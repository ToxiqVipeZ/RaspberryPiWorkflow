import tkinter as tk
import sqlite3
import re


class WorkflowPlannerApp:
    """
    This class creates an App to plan and manage the workflow of a procedure
    """

    def take_input(self, root, text_window, operation):
        """
        Checks which input window to process into the database operations
        :param root: main window
        :param text_window: which text window is given
        :param operation: what operation to execute
        """
        if operation == "save":
            text_input = text_window.get("1.0", "end-1c")
            self.database_save(root, text_input)
        if operation == "delete":
            text_input = text_window.get()
            if len(text_input) != 3:
                self.message_label(root, "Fehlerhaften Eingabe, Zeichenlänge ist nicht 3")
            else:
                self.database_delete(root, text_input)

    @staticmethod
    def message_label(root, message):
        """
        Generalized method to print messages into the main window
        :param root: main window
        :param message: which message to display
        """
        text_label = tk.Label(root, text=message)
        text_label.config(font=("Courier", 14))
        text_label.pack()
        text_label.update()
        text_label.after(2000, text_label.destroy())

    @staticmethod
    def delete_input_checker(input_to_check):
        """
        Checks if the input of the text to delete only contains digits
        :param input_to_check: the input to check
        :return: true when the input only contains digits
        """
        if input_to_check.isdigit():
            return True
        else:
            return False

    def database_save(self, root, text_input):
        """
        The method that executes write operations into the database
        :param root: main window (for user feedback)
        :param text_input: what to write into the database (workflow_procedure & stations_values
        """
        try:
            # connection holds the connection to the database
            # (path\productionDatabase.db)
            connection = sqlite3.connect(
                "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

            # cursor instance:
            c = connection.cursor()

            regex = "^[0-9]{3}(;{1}[0-9]{2})+"

            if re.search(regex, text_input):
                workflow_procedure_value = text_input.split(";")
                workflow_procedure_value = workflow_procedure_value[:1]
                workflow_procedure_value = ";".join([str(item) for item in workflow_procedure_value])

                stations_values = text_input.split(";")
                stations_values = stations_values[1:]
                stations_values = ";".join([str(item) for item in stations_values])
                print(stations_values.endswith(";"))
                if stations_values.endswith(";"):
                    stations_values = stations_values[:-1]

                # workflow_procedure_value = procedure number (examples: 001, 002, 003)
                # stations_value = station number (multiple: [01;02;05, 07;02;01;05,03 ...])
                c.execute("INSERT INTO workflow_planner_table VALUES (?, ?)",
                          (workflow_procedure_value, stations_values))

                print(workflow_procedure_value)
                print(stations_values)

                self.message_label(root, "Prozessablauf gespeichert.")
            else:
                self.message_label(root, "Fehlerhafte Eingabe.")

            # committing the created table:
            connection.commit()

            # closing the connection
            connection.close()

        except sqlite3.IntegrityError:
            self.message_label(root, "Verfahren bereits angelegt.")

    @staticmethod
    def database_delete(root, text_input):
        """
        The method that executes delete operations into the database
        :param root: main window (for user feedback)
        :param text_input: what to delete out of the database (workflow_procedure)
        :return:
        """
        # connection holds the connection to the database
        # (path\productionDatabase.db)
        connection = sqlite3.connect(
            "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

        # cursor instance:
        c = connection.cursor()

        print(text_input)
        c.execute("DELETE FROM workflow_planner_table WHERE workflow_planner_table.workflow_procedure = (?)",
                  (text_input,))

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
        The main-window, displaying all functional input fields, buttons and labels
        """
        # loop of the window - START
        root = tk.Tk()

        width, height = root.winfo_screenwidth(), root.winfo_screenheight()

        # window size
        # canvas_root = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        # window grid
        # canvas_root.grid(columnspan=3, rowspan=3)

        text_save_window = tk.Text(root, height=5, width=40)
        text_label = tk.Label(root, text="Form: \"Verfahren;Fertigung;Montage;Versand;...\""
                                         "\n Beispiel: 001;01;02;05;...")
        text_label.config(font=("Arial", 14))
        text_label.pack(pady=(10, 0))
        text_save_window.pack(pady=(0, 10))

        root.geometry("%dx%d+0+0" % (width, height))

        # button_save definition
        button_save_text = tk.StringVar()
        button_save_text.set("Save")
        button_save_btn = tk.Button(root, textvariable=button_save_text,
                                    command=lambda: (self.take_input(root, text_save_window, "save")),
                                    width=8, height=1, background="green", font=("Arial", 14))
        # buttonTest_btn.grid(column=0, row=0)
        button_save_btn.pack(pady=(5, 10))

        # spaceholder
        spaceholder = tk.Label(root, width=5, height=5)
        spaceholder.pack(pady=(10, 10))

        text_delete_window = tk.Entry(root, width=40)
        text_label = tk.Label(root, text="Eintrag entfernen: Verfahren"
                                         "\n Beispiel: 001")
        text_label.config(font=("Arial", 14))
        text_label.pack(pady=(10, 0))
        text_delete_window.pack(pady=(0, 10))

        # button_save definition
        button_delete_text = tk.StringVar()
        button_delete_text.set("Delete")
        button_delete_btn = tk.Button(root, textvariable=button_delete_text,
                                      command=lambda: (self.take_input(root, text_delete_window, "delete")),
                                      width=8, height=1, background="green", font=("Arial", 14))

        # buttonTest_btn.grid(column=0, row=0)
        button_delete_btn.pack(pady=(5, 10))

        delete_input_check = root.register(self.delete_input_checker)
        text_delete_window.config(validate="key", validatecommand=(delete_input_check, "%P"))

        # loop of the window - END!
        root.mainloop()


WorkflowPlannerApp().main()
