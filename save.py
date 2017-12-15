import os.path # Check if file exists
import csv # For DictWriter

# Check if file exists, if so put a number behind it
def check_file(filename, extension='.csv'):
    num = 2
    if os.path.isfile(filename + extension):
        num = 2
        while(os.path.isfile(filename + str(num) + extension)):
            num += 1
        filename += '-'+str(num)
    return filename + extension

def write_dict(mydict, filename):
    # print("Saving dictionary to:", filename)
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in mydict.items():
           writer.writerow([key, value])

def read_dict(filename):
    # print("Reading dictionary from:", filename)
    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)
        return mydict

def save_distribution(unique, counts, filename):
    folder = 'results/dist/'
    if not os.path.isdir(folder): os.mkdir(folder)
    filename = check_file(folder + filename)
    # print("Saving distribution to", filename)
    with open(filename, 'w') as file:
        for i in range(int(len(unique))):
            file.write(str(int(unique[i]))+","+str(counts[i])+"\n")

def save_measure(measure, filename):
    folder = 'results/measures/'
    if not os.path.isdir(folder): os.mkdir(folder)
    outputfile = check_file(folder + db + '_' + filename)
    # print("Saving measure to:", outputfile)
    with open(outputfile, 'w') as file:
        for key in measure:
            file.write(str(key)+","+str(float(measure[key]))+"\n")
