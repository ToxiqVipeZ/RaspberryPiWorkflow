

class CassetteScanner:
    triggered_cassette = 0

    def get_triggered_cassette(self):
        return self.triggered_cassette

    def set_triggered_cassette(self, triggered):
        self.triggered_cassette = triggered

    def main(self):
        pass

if __name__ == '__main__':
    CassetteScanner().main()
