from PyPDF2 import PdfReader
import os


class PdfFile:
    def __init__(self, folder_name):
        self.folder_name = folder_name
        self.files = []
        self.p_join = os.path.join

    def get_file_names(self):
        for file in os.listdir(self.folder_name):
            if not file.endswith(".pdf"):
                raise IsADirectoryError(
                    f"\"{self.folder_name}\": This dir should" +
                    " contain only pdf files")
            file = self.p_join(self.folder_name, file)
            new_name = self.extract_text(file)

            self.files.append((file,
                              self.p_join(self.folder_name, new_name)))
        self.rename()

    def extract_text(self, name):
        reader = PdfReader(name)
        page = reader.pages[0]
        new_lines = page.extract_text().split("\n")
        month = None

        for line in new_lines:
            if "Περίοδος:".casefold() in line.casefold():
                month = line.split(":")
                break
        else:
            raise ValueError("The text wasn't found.")
        month[-1].strip()
        month = month[-1].split()
        return "_".join(month)

    def rename(self):
        for old, new in self.files:
            os.rename(old, new)


pdf = PdfFile(
    "/home/xaos/projects/python/month-payment-checker/datafiles/pdfs/")
pdf.get_file_names()
