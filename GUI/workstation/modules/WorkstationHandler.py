try:
    from modules.Reader import Reader
except ImportError:
    print("Reader import failed, check correct file location.")
    
try:
    from modules.Writer import Writer
except ImportError:
    print("Reader import failed, check correct file location.")
    
try:
    from threading import Thread
except ImportError:
    print("Thread import failed.")


class WorkstationHandler:
    rfid_scanned = None
    written_flag = False

    def __init__(self):
        self.rfid_scan = ""
        self.rfid_scanned = ""
        
    def get_rfid(self):
        return self.rfid_scanned

    def reading_op(self):
        read = Reader()
        read.reader()
        self.rfid_scanned = read.get_result()
        read.reset_result()
    
    def reset_rfid(self):
        self.rfid_scanned = ""

    def writing_op(self, value):
        Writer(value)
        self.written_flag = True

    def start_op(self, op, *args):
        if op == "reader_start":
            thread_reader = Thread(target=self.reading_op())
            thread_reader.start()

        elif op == "writer_start":
            thread_writer = Thread(target=self.writing_op(args[0]))
            thread_writer.start()
            
        elif op == "reset_rfid":
            thread_reset = Thread(target=self.reset_rfid())
            thread_reset.start()




