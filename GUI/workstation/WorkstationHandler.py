import Reader
from Writer import Writer
from threading import Thread


class WorkstationHandler:
    rfid_scanned = None

    def __init__(self):
        self.rfid_scan = ""
        self.rfid_scanned = ""
        
    def get_rfid(self):
        return self.rfid_scanned

    def reading_op(self):
        read = Reader.Reader()
        read.reader()
        self.rfid_scanned = read.get_result()
        read.reset_result()
    
    def reset_rfid(self):
        self.rfid_scanned = ""

    def writing_op(self, value):
        Writer(value)

    def start_op(self, op, *args):
        if op == "reader_start":
            thread_reader = Thread(target=self.reading_op())
            thread_reader.start()

        elif op == "writer_start":
            thread_writer = Thread(target=self.writing_op(args[1]))
            thread_writer.start()
            
        elif op == "reset_rfid":
            thread_reset = Thread(target=self.reset_rfid())
            thread_reset.start()




