import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


f = open("3.2.7 Investigating Data - Ques 5.csv", 'r') #Open file
fig, ax = plt.subplots()        #setup subplots

x = np.arange(29)
names = [] #Create empty lists
y = []

lineNumber = 1 #Line counter
for line in f: #Iterate through pertinent lines in file
    if lineNumber > 1 and lineNumber < 32 and lineNumber!= 11:
        line = line.strip()
        line = line.split(",")
        names.append(line[1]) #Append data to lists
        y.append(float(line[9]))
    lineNumber += 1

print stats.f_oneway(1,2,3,4,5)

barlist = ax.bar(x,y) #Set custom colors for each bar
barlist[0].set_color('#E13A3E')
barlist[1].set_color('#008348')
barlist[2].set_color('#061922')
barlist[3].set_color('#008CA8')
barlist[4].set_color('#CE1141')
barlist[5].set_color('#860038')
barlist[6].set_color('#007DC5')
barlist[7].set_color('#FDB927')
barlist[8].set_color('#ED174C')
barlist[9].set_color('#CE1141')
barlist[10].set_color('#FFC633')
barlist[11].set_color('#006BB6')
barlist[12].set_color('#552582')
barlist[13].set_color('#0F586C')
barlist[14].set_color('#98002E')
barlist[15].set_color('#00471B')
barlist[16].set_color('#005083')
barlist[17].set_color('#B4975A')
barlist[18].set_color('#F58426')
barlist[19].set_color('#F05133')
barlist[20].set_color('#007DC5')
barlist[21].set_color('#ED174C')
barlist[22].set_color('#E56020')
barlist[23].set_color('#E03A3E')
barlist[24].set_color('#724C9F')
barlist[25].set_color('#BAC3C9')
barlist[26].set_color('#CE1141')
barlist[27].set_color('#00471B')
barlist[28].set_color('#002B5C')

ax.set_xticks(x+.3) #Format and set axis labels
ax.set_xticklabels((names), rotation=45)
ax.set_xlim([0,29])
ax.set_ylim([0,32])
plt.title('Stephen Curry\'s Performance vs. NBA Teams') #Add title
plt.xlabel('Team Name')
plt.ylabel('Points per Game')
plt.show() #Display graph