import os
import csv

normed_data_path = os.path.abspath('normed_data.csv')
def norm_data():
    reader = csv.reader(file('data.csv'))
    count = -1
    vals_1900 = ['1384', '151', '543', '308', '68', '3815', '5881', '112', '1589', '155', '88', '55', '1708', '995', '192', '101', '140']
    norms = [ int(xx) for xx in vals_1900 ] 

    writer = csv.writer(file(normed_data_path, 'w'))

    for line in reader:
        count += 1
        if count == 0:
            writer.writerow(line)
        else:
            newline = []
            newline.append(line[0])
            for ii in range(len(line[1:])):
                if line[ii + 1]:
                    val = 100 * float(line[ii + 1]) / float(norms[ii])
                    newline.append(val)
                else:
                    newline.append(line[ii + 1])
            writer.writerow(newline)

def plot_plain():
    cmd = 'pl -png -prefab lines -o govt_finance.png data=data.csv x=1 y=2 y2=3 y3=4 delim=comma header=yes "plotsym=none"'
    os.system(cmd)

def plot_normed():
    norm_data()
    cmd = 'pl -png -prefab lines -o govt_finance_normed.png data=%s x=1 y=14 y2=7 y3=8 y4=18 delim=comma header=yes' 
    cmd = cmd % normed_data_path
    os.system(cmd)
    os.remove(normed_data_path)

if __name__ == '__main__':
    # plot_plain()
    plot_normed()
