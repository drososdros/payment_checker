import os


class Settings:
    def __init__(self):
        self.dest_folder = "../../month-payment-checker/main/data/"
        self.src_folder = "../../month-payment-checker/main/input/"
        self.dest_pdfs = os.path.join(self.dest_folder, "pdfs")
        self.src_pdfs = os.path.join(self.src_folder, "pdfs")

        self.dest_csv = self.dest_folder
        self.src_csv = os.path.join(self.src_folder, "csvs")
