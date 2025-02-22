from compare import Compare
from csv_data import CsvData
from pdf_data import PdfFile


def main():
    csv = CsvData()
    csv.extract_csv_data()
    pdf = PdfFile()
    pdf.extract_data()
    comp = Compare(csv.data, pdf.data)
    comp.results()


if __name__ == "__main__":
    main()
