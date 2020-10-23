import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

def load_data(filename):
    #Open de CSV file and save it in reader variable
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        evidence=[]
        label=[]
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        for row in reader:
            #Change months in string to int type
            for i in range(len(months)):
                if row[10]==months[i]:
                    aux=i
                    break
            #Appending data into evidence list
            evidence.append([
                int(row[0]), float(row[1]),int(row[2]),float(row[3]),int(row[4]), float(row[5]),float(row[6]),float(row[7]),float(row[8]) ,float(row[9]),aux,int(row[11]), int(row[12]), int(row[13]),int(row[14]), 1 if row[15] == "New_Visitor" else 0, 1 if row[16] == "TRUE" else 0
            ])
            label.append([
                1 if row[17] == "TRUE" else 0
            ])
    #Return a tuple
    return (evidence, label)
if __name__ == "__main__":
    main()
