import numpy as np
import matplotlib.pyplot as plt

f = open("3.2.7 Investigating Data - Ques 3.csv", 'r') #Open file
fig, ax = plt.subplots()        #setup subplots
width = 0.11
x = np.array([0,1,2,3,4,5])

nov, dec, jan, feb, mar, apr = [], [], [], [], [], []                        #blank lists for months
colors = ['#006bb6', '#fdb927', '#bebebe', '#000000', '#ff0000', '#001b66', '#fff390']  #list of colors for bars
rects = []          #helps in making the legend

lineNumber = 1
for line in f:      #iterate through useful lines in csv
    if lineNumber > 1 and lineNumber < 9:
        line = line.strip()
        line = line.split(",")
        #arg1: list setting x-values for left side of bars. lineNumber-2 is multiplier that determines the offset
        #      so bars aren't all on top of each other
        #arg 2: picks middle six values of line.
        #arg 3: determines width of bar                arg 4: determines color
        rect = ax.bar(x+width*(lineNumber-2), line[1:7], width, color = colors[lineNumber-2])
        ax.set_xticks(x+width*3.5)                                          #format x-axis
        ax.set_xticklabels(('Oct-Nov','Dec','Jan','Feb','Mar','Apr'))
        nov.append(line[1])                 #stores plotted data in lists for later calculation
        dec.append(line[2])
        jan.append(line[3])
        feb.append(line[4])
        mar.append(line[5])
        apr.append(line[6])
        rects.append(rect[0])               #takes sample bar from each subplot for use of its color in legend
    lineNumber += 1

def show_avg(month, offset):                #function displaying average PPG for each month overall in career
    month[:] = [float(x) for x in month if float(x) != 0.0]     #get rid of 0s representing months w/ 0 games played
    total, avg = 0.0, 0.0
    for num in month:               #calculate average PPG for each month and display above bar cluster
        total += num
    avg = total/len(month)
    height = max(month)
    ax.text(offset + width*3.5 - 0.18, 1.02*height, round(avg,1))   #numbers are through trial and error
                                                                    #first arg: x-position of textbox; second arg: y; third box: text itself
                
show_avg(nov, 0)            #display avg for each month
show_avg(dec, 1)
show_avg(jan, 2)
show_avg(feb, 3)
show_avg(mar, 4)
show_avg(apr, 5)

plt.title('Points per Game by Month')               #touch up graph and display it
ax.set_ylim([0,45])
plt.xlabel('Month')
plt.ylabel('PPG')
ax.legend(rects, ('2009-10','2010-11','2011-12','2012-13','2013-14','2014-15','2015-16'), loc='upper left', ncol=3)
plt.show()