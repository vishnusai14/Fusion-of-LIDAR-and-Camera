import matplotlib.pyplot as plt
import csv


r = []
thetha = []

with open('./data.csv', 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        print(row)
        if len(row) != 0:
            r.append(float(row[0]))
            thetha.append(float(row[1]))
            





fig = plt.figure()
ax = fig.add_subplot(111, projection = "polar")
ax.scatter(thetha, r)
plt.show()