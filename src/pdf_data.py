from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
import os

greek_to_english_months = {
    "Ιανουάριος": "January",
    "Φεβρουάριος": "February",
    "Μάρτιος": "March",
    "Απρίλιος": "April",
    "Μάιος": "May",
    "Ιούνιος": "June",
    "Ιούλιος": "July",
    "Αύγουστος": "August",
    "Σεπτέμβριος": "September",
    "Οκτώβριος": "October",
    "Νοέμβριος": "November",
    "Δεκέμβριος": "December",
    "Απριλίου": "April",
    "Ιουλίου": "July",
    "Δεκεμβρίου": "December",
}


class PdfData:
    def __init__(self, text, current_filename) -> None:

        self.text = text
        self.current_filename = current_filename
        self.new_name = None
        self.salary_advance = None
        self.salary_payment = None
        self.date = None
        self._new_name()
        if self.date is None:
            raise ValueError(
                f"{self.__class__.__name__}: Date should not be none")

        if self.salary_advance is None:
            raise ValueError(
                f"{self.__class__.__name__}: salary advance should not be none")
        if self.salary_payment is None:
            raise ValueError(
                f"{self.__class__.__name__}: salary payment should not be none")

    def _new_name(self):
        all_data = self.text.split("\n")
        for data in all_data:
            if self.date and self.salary_payment and self.salary_advance\
                    and self.new_name:
                break
            if "Περίοδος:".casefold() in data.casefold():
                greek_name = data.split(":")[-1].split()
                name = greek_to_english_months.get(greek_name[-2])
                self.new_name = "_".join(greek_name) + ".pdf"
                if name is None:
                    raise KeyError(
                        f"{greek_name[-2]} not found in" +
                        " the greek_to_english_months")
                self.date = datetime.strptime(
                    f"10/{name}/{greek_name[-1]}", "%d/%B/%Y")

            if "ΠΡΟΚΑΤΑΒΟΛΗ".casefold() in data.casefold():
                salary = data.split()[-1]
                self.salary_advance = salary

            if "ΥΠΟΛΟΙΠΟ ΠΛΗΡΩΤΕΩΝ ΑΠΟΔΟΧΩΝ".casefold() in data.casefold():
                self.salary_payment = data.split()[-1]

    def __eq__(self, o):
        return self.new_name == o.new_name \
            and self.date == o.date

    def __gt__(self, o):
        return self.date > o.date

    def __str__(self):
        return f"{self.current_filename}, {self.date}, {self.new_name}"


class PdfFile:
    def __init__(self, settings):
        self.settings = settings
        self.data = []
        self.p_join = os.path.join

    def extract_data(self):
        for file in os.listdir(self.settings.src_pdfs):
            pdf_path = os.path.join(self.settings.src_pdfs, file)
            pdf = PdfReader(pdf_path)
            pages = pdf.pages

            if len(pages) > 1:
                for page in pages:
                    wr_pdf = PdfWriter()
                    data = PdfData(page.extract_text(), file)
                    new_name = data.new_name
                    data.current_filename = new_name
                    wr_pdf.add_page(page)
                    wr_pdf.write(self.p_join(self.settings.src_pdfs, new_name))
                    if data not in self.data:
                        self.data.append(data)
                os.remove(self.p_join(self.settings.src_pdfs, file))
            else:

                data = PdfData(pages[0].extract_text(), file)
                if data not in self.data:
                    self.data.append(data)
