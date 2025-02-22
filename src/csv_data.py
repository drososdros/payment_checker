import os


class CsvData:
    pass

    def __init__(self) -> None:
        self.folder_name = "./input/csvs/"
        self.data = []
        self.p_join = os.path.join
        self.employer_names = {"G.ΗΙGΑS", "ΧΙΓΚΑΣ", "G.Η"}

    def in_employer_names(self, line):
        for i in self.employer_names:
            if i in line:
                return True
        return False

    def extract_csv_data(self):
        for file in os.listdir(self.folder_name):
            if not file.casefold().endswith(".csv".casefold()):
                raise IsADirectoryError(
                    f"\"{self.folder_name}\": This dir should" +
                    " contain only .csv files")

            file = self.p_join(self.folder_name, file)
            with open(file, "r") as fl:
                file = fl.readlines()
            for line in file:
                if ";Π;" in line:
                    bank_data = BankData(line)
                    if bank_data not in self.data and self.in_employer_names(bank_data.message):
                        self.data.append(bank_data)


class BankData:
    def __init__(self, line=None) -> None:
        self.line = line
        self.date = ""
        self.amount = ""
        self.message = ""
        self.set_bank_data()

    def set_bank_data(self):
        if not self.line:
            raise ValueError("BankData: line shouldn't be empty")
        line = self.line.split(";")
        self.date = line[1]
        self.message = line[2]
        self.amount = line[-3]

    def __str__(self) -> str:
        return str(self.line)

    def __eq__(self, o):
        return self.date == o.date \
            and self.amount == o.amount \
            and self.message == o.message

    def __lt__(self, o):
        this = self.date.split("/")
        other = o.date.split("/")
        return this[2] < other[2] \
            or this[2] == other[2] and this[1] < other[1] \
            or (this[2] == other[2] and this[1] == other[1]
                and this[0] < other[0])

    def __gt__(self, o):
        this = self.date.split("/")
        other = o.date.split("/")
        return this[2] > other[2] \
            or this[2] == other[2] and this[1] > other[1] \
            or (this[2] == other[2] and this[1] == other[1]
                and this[0] > other[0])

    def __repr__(self) -> str:
        return (f"date: {self.date}, ammount: {self.amount}," +
                f" message: {self.message}")


i = CsvData()
i.extract_csv_data()
