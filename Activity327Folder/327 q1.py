import numpy as np
import matplotlib.pyplot as plt

f = open("3.2.7 Investigating Data - Ques1.csv", 'r') #Open file
fig, ax = plt.subplots()

ppg = []            #empty lists
seasons = []

for line in f:     #Iterate through lines of file
    line = line.strip()
    line = line.split(",")
    if (line[1] != '') and (line[1] != 'PPG'):            # only add cells from rows with numbers to lists
        ppg.append(line[1])
        seasons.append(line[0])

x = np.arange(len(seasons))                 #x values of plot
plt.plot(x, ppg, color='#fdb927')         #format plot
ax.set_xticklabels(seasons)
plt.xlabel('Season')
plt.ylabel('Points per Game')
plt.ylim([0,35])
plt.title("Curry's PPG Over his NBA Career")
plt.grid(b=True, which='major', color='#003b86', linestyle='-')
plt.grid(b=True, which='minor', color='#003b86', linestyle=':')
plt.minorticks_on()
plt.show()