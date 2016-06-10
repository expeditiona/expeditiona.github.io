import numpy as np
import matplotlib.pyplot as plt

f = open("3.2.7 Investigating Data - Ques 4.csv", 'r') #Open file
fig, ax = plt.subplots()

x = np.arange(11)           #x values and blank lists
names = []
figs = []
lineNumber = 1
for line in f:              #iterate thru lines
    line = line.strip()
    line = line.split(",")
    if lineNumber > 1 and lineNumber < 13:  #add cells from appropriate rows to blank lists
        names.append(line[0])
        figs.append(line[1])
    lineNumber+=1

barlist=ax.bar(x+0.2, figs)             #create bar graph and color each bar the player's team color
barlist[10].set_color('#fdb927')        
barlist[9].set_color('#fdb927')         
barlist[8].set_color('#ce1141')         
barlist[7].set_color('#b6bfbf')         
barlist[6].set_color('#552582')         
barlist[5].set_color('#00275d')         
barlist[4].set_color('#860038')         
barlist[3].set_color('#006bb6')         
barlist[2].set_color('#b6bfbf')         
barlist[1].set_color('#007dc5')
barlist[0].set_color('#f05133')

plt.xlabel('Player')                #axis titles and x-axis formatting
plt.ylabel('Made 3s')
plt.title('Top 3-Pt Shooters in the NBA 2015-16')
plt.xticks((0.5,1.5,2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5), rotation=25)
ax.set_xticklabels(names)
plt.show()