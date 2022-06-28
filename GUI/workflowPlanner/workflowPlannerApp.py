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
        # if the passed operation is called "save"
        if operation == "save":
            text_input = text_window.get("1.0", "end-1c")
            # the textinput that needs to be saved gets passed to database_save
            self.database_save(root, text_input)

        # if the passed operation is called "save"
        if operation == "times":
            text_input = text_window.get("1.0", "end-1c")
            # the textinput that needs to be saved gets passed to database_save
            self.database_save_times(root, text_input)

        # if the passed operation is called "delete"
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

    def article_procedure_popup(self, root):
        popup = tk.Toplevel(root, )
        popup_article_label = tk.Label(popup, text="Artikel-ID:")
        popup_procedure_label = tk.Label(popup, text="Vorgangsnummer:")
        article_entry = tk.Entry(popup)
        procedure_entry = tk.Entry(popup)
        popup_confirm_button = tk.Button(popup,
                                         text="Speichern",
                                         command=lambda: (
                                             self.article_procedure_database_operation(
                                                 article_entry.get(),
                                                 procedure_entry.get(),
                                                 popup)
                                         ))
        popup_article_label.pack()
        article_entry.pack()
        popup_procedure_label.pack()
        procedure_entry.pack()
        popup_confirm_button.pack()

    def article_procedure_database_operation(self, value_a, value_b, window):
        print(value_a)
        print(value_b)
        print(self.delete_input_checker(value_a))
        print(self.delete_input_checker(value_b))
        if (self.delete_input_checker(value_a) & self.delete_input_checker(value_b)) == True:
            # database operation:
            connection = sqlite3.connect(
                "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")
            c = connection.cursor()
            c.execute("INSERT INTO article_procedure_table VALUES (?, ?)",
                      (value_a, value_b))
            connection.commit()
            connection.close()
        else:
            pass
            self.message_label(window, "Fehlerhafte Angaben. Bitte erneut versuchen.")

    def database_save_times(self, root, text_input):
        """
        The method that executes write operations into the database
        :param root: main window (for user feedback)
        :param text_input: what to write into the database (workflow_procedure & stations_values
        """
        try:
            # connection holds the connection to the database
            # (path/productionDatabase.db)
            connection = sqlite3.connect(
                "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

            # cursor instance:
            c = connection.cursor()

            # the format that the input has to be in
            regex = "^[0-9]{3}(;{1}[0-9]{2})+"

            # looking if the given input matches the regex
            if re.search(regex, text_input):
                workflow_procedure_value = text_input.split(";")
                workflow_procedure_value = workflow_procedure_value[:1]
                workflow_procedure_value = ";".join([str(item) for item in workflow_procedure_value])

                times = text_input.split(";")
                times = times[1:]
                times = ";".join([str(item) for item in times])

                # delete the last ";" if there is one given at the end of declaration
                if times.endswith(";"):
                    times = times[:-1]

                # workflow_procedure_value = procedure number (examples: 001 | 002 | 003)
                # stations_value = station number (examples: [01;02;05] | [07;02;01;05,03] | ...])
                c.execute("UPDATE workflow_planner_table SET times=(?) WHERE workflow_procedure=(?)",
                          (times, workflow_procedure_value))

                print(workflow_procedure_value)
                print(times)

                self.message_label(root, "Prozessablauf gespeichert.")
            else:
                self.message_label(root, "Fehlerhafte Eingabe.")

            # committing the created table:
            connection.commit()

            # closing the connection
            connection.close()

        except sqlite3.IntegrityError:
            self.message_label(root, "Zeiten bereits angelegt.")

    def database_save(self, root, text_input):
        """
        The method that executes write operations into the database
        :param root: main window (for user feedback)
        :param text_input: what to write into the database (workflow_procedure & stations_values
        """
        try:
            # connection holds the connection to the database
            # (path/productionDatabase.db)
            connection = sqlite3.connect(
                "C:/Users/g-oli/PycharmProjects/RaspberryPiWorkflow/Database/productionDatabase.db")

            # cursor instance:
            c = connection.cursor()

            # the format that the input has to be in
            regex = "^[0-9]{3}(;{1}[0-9]{2})+"

            # looking if the given input matches the regex
            if re.search(regex, text_input):
                workflow_procedure_value = text_input.split(";")
                workflow_procedure_value = workflow_procedure_value[:1]
                workflow_procedure_value = ";".join([str(item) for item in workflow_procedure_value])

                stations_values = text_input.split(";")
                stations_values = stations_values[1:]
                stations_values = ";".join([str(item) for item in stations_values])

                # delete the last ";" if there is one given at the end of declaration
                if stations_values.endswith(";"):
                    stations_values = stations_values[:-1]

                # workflow_procedure_value = procedure number (examples: 001 | 002 | 003)
                # stations_value = station number (examples: [01;02;05] | [07;02;01;05,03] | ...])
                c.execute("INSERT INTO workflow_planner_table(workflow_procedure, stations) VALUES (?, ?)",
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

        # saving screen width and height
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()

        # textbox to save a procedure workflow
        text_save_window = tk.Text(root, height=5, width=40)
        # label above the text_save_window
        text_label = tk.Label(root, text="Form: \"Verfahren;Fertigung;Montage;Versand;...\""
                                         "\n Beispiel: 001;01;02;05;...")
        text_label.config(font=("Arial", 14))
        text_label.pack(pady=(10, 0))
        text_save_window.pack(pady=(0, 10))

        # button_save definition
        button_save_text = tk.StringVar()
        button_save_text.set("Save")
        # when the save button is pressed, take_input gets called
        button_save_btn = tk.Button(root, textvariable=button_save_text,
                                    command=lambda: (self.take_input(root, text_save_window, "save")),
                                    width=8, height=1, background="green", font=("Arial", 14))
        # buttonTest_btn.grid(column=0, row=0)
        button_save_btn.pack(pady=(5, 10))

        # textbox to save a procedure workflow
        text_save_times_window = tk.Text(root, height=5, width=40)
        # label above the text_save_window
        text_times_label = tk.Label(root, text="Zeiten in Sekunden pro Station: \n"
                                               "30, 30, 45, 55 ...")
        text_times_label.config(font=("Arial", 14))
        text_times_label.pack(pady=(10, 0))
        text_save_times_window.pack(pady=(0, 10))

        # applying screen width and height to the window size
        root.geometry("%dx%d+0+0" % (width, height))

        # button_save definition
        button_save_times_text = tk.StringVar()
        button_save_times_text.set("Save Times")
        # when the save button is pressed, take_input gets called
        button_save_times_btn = tk.Button(root, textvariable=button_save_times_text,
                                    command=lambda: (self.take_input(root, text_save_times_window, "times")),
                                    width=8, height=1, background="green", font=("Arial", 12))
        # buttonTest_btn.grid(column=0, row=0)
        button_save_times_btn.pack(pady=(5, 10))

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

        button_relation_text = tk.StringVar()
        button_relation_text.set("Artikel<->Vorgang")
        button_relation_btn = tk.Button(root, textvariable=button_relation_text,
                                        command=lambda: (self.article_procedure_popup(root)),
                                        width=15, height=2, background="green", font=("Arial", 14))
        button_relation_btn.pack(pady=(5, 10))

        delete_input_check = root.register(self.delete_input_checker)
        text_delete_window.config(validate="key", validatecommand=(delete_input_check, "%P"))

        # loop of the window - END!
        root.mainloop()


WorkflowPlannerApp().main()
