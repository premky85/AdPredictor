import csv

def read_data(t, file):
    tabela = []
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        for row in csv_reader:
            p = []
            for i in t:
                p.append(row[i])
            tabela.append(p)

    return tabela




