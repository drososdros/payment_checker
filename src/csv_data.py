import os
from datetime import datetime


class CsvData:

    def __init__(self, settings) -> None:
        self.settings = settings
        self.data = []
        self.finished = []
        self.p_join = os.path.join
        self.employer_names = {"G.ΗΙGΑS", "ΧΙΓΚΑΣ", "G.Η", "Γ.ΧΙΓΚΑΣ"}

    def in_employer_names(self, line):
        for i in self.employer_names:
            if i in line:
                return True
        return False

    def extract_csv_data(self):
        for file in os.listdir(self.settings.src_csv):
            if not file.casefold().endswith(".csv".casefold()):
                raise IsADirectoryError(
                    f"\"{self.settings.src_csv}\": This dir should" +
                    " contain only .csv files")

            file = self.p_join(self.settings.src_csv, file)
            with open(file, "r") as fl:
                file = fl.readlines()
            for line in file:
                if ";Π;" in line:
                    bank_data = BankData(line)
                    if bank_data not in self.data and self.in_employer_names(
                            bank_data.message):
                        self.data.append(bank_data)


class BankData:
    def __init__(self, line=None) -> None:
        self.line = line
        self.date = None
        self.amount = ""
        self.message = ""
        self.set_bank_data()

    def set_bank_data(self):
        if not self.line:
            raise ValueError("BankData: line shouldn't be empty")
        line = self.line.split(";")
        self.date = datetime.strptime(line[1] + " 00:00", "%d/%m/%Y %H:%M")
        self.message = line[2]
        self.amount = line[-3]

    def __str__(self) -> str:
        return str(self.line)

    def __eq__(self, o):
        if isinstance(o, BankData):
            return self.date == o.date \
                and self.amount == o.amount \
                and self.message == o.message
        if isinstance(o, datetime):
            return self.date == o
        if isinstance(o, int):
            if self.date is not None:
                return self.date.month == o
        return False

    def __lt__(self, o):
        return self.date < o.date

    def __gt__(self, o):
        return self.date > o.date

    def __repr__(self) -> str:
        return (f"date: {self.date}, ammount: {self.amount}," +
                f" message: {self.message}")
