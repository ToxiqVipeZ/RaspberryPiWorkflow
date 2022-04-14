import WorkstationApp
import workflowPagesDisplay


class WindowController(object):
    rfid_scanned = 0

    def __init__(self, rfid_scanned):
        self.rfid_scanned = rfid_scanned

