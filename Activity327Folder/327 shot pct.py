import matplotlib.pyplot as plt
f = open("3.2.7 Investigating Data - Ques 2.csv", 'r') #Open file

spot = [] #Create empty lists
pct = []
shotpct = []
combined = [] 

lineNumber = 1

for line in f: #Iterate through lines of file
    line = line.strip()
    if lineNumber > 1 and lineNumber < 9: 
        spot.append(line.split(",")[0]) #Append data to lists
        pct.append(line.split(",")[1])
        shotpct.append(line.split(",")[2])
    lineNumber += 1 

for x in range(7):
    combined.append(spot[x] + ': ' + shotpct[x] + ' FG pct.') #Format labels
    


colors = ['#fdb927', '#006bb6', '#fdb927','#006bb6', '#fdb927', '#006bb6','#ffffff'] #Warriors colors



fig, ax = plt.subplots(1, 1)
explode = (0.1,0.1,0.1,0.1,0.1,0.1,0.1)

ax.pie(pct, labels=combined, colors=colors, autopct='%.0f%%', explode = explode )

ax.set_aspect(1) #Square axes for round plot

ax.set_title('Shooting Percentage and Distribution of Stephen Curry\'s Shots in 2015-16')

fig.show() #Display pie chart