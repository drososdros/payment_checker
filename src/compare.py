from datetime importtimedelta
import os
from shutil import move


class Finished:
    def __init__(self, pdf, csv, csv2):

        self.pdf = pdf
        self.csv = csv
        self.csv2 = csv2

    def __str__(self):
        return f"{self.pdf}, {self.csv}, {self.csv2}"


class Compare:
    def __init__(self, csv_data, pdf_data):
        self.csv = sorted(csv_data)
        self.pdf = sorted(pdf_data)
        self.dest = "../../month-payment-checker/main/data/pdfs/"
        self.finished = []
        if not self.csv or not self.pdf:
            print("there is nothing to do here")
            exit(0)

    def compare_advance(self, pdf, csv):
        return pdf.date.month == csv.date.month \
            and pdf.date.year == csv.date.year \
            and pdf.salary_advance == csv.amount

    def compare_salary(self, pdf, csv):
        return csv.date > pdf.date \
            and csv.date < pdf.date + timedelta(days=30) \
            and pdf.salary_payment == csv.amount

    def results(self):
        for pdf in self.pdf:
            pay1, pay2 = None, None

            for csv in self.csv:

                if pdf.salary_advance == "0,00":
                    pay1 = True
                elif self.compare_advance(pdf, csv):
                    pay1 = csv

                if self.compare_salary(pdf, csv):
                    pay2 = csv
                # input(#)
                if pay1 and pay2:
                    finish = Finished(pdf, pay1, pay2)
                    self.finished.append(finish)
                    if pay1 is True:
                        pass
                    else:
                        self.csv.remove(pay1)
                    self.csv.remove(pay2)
                    break

        filename = "../../month-payment-checker/main/input/pdfs/"
        mv_filename = "../../month-payment-checker/main/data/"
        with open(os.path.join(mv_filename, "found.csv"), "a") as fl:
            for i in self.finished:
                filename = "../../month-payment-checker/main/input/pdfs/"
                mv_filename = "../../month-payment-checker/main/data/"
                src = os.path.join(filename, i.pdf.current_filename)
                dest = os.path.join(mv_filename, "pdfs", i.pdf.new_name)
                move(src, dest)
                fl.write(str(i.csv))
                fl.write(str(i.csv2))

        with open(os.path.join(mv_filename, "Notfound.csv"), "a") as fl:
            for i in self.csv:
                fl.write(str(i))
