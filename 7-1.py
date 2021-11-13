import numpy as np
import matplotlib.pyplot as plt

"""
Posiciones:
0 -> Step
1 -> state
2 (3) -> interval [no usar]
4 -> reward
5 -> acc_reward
6 -> freqpos
7 -> frequency
8 -> power
"""

def get_file_data(csv):
    csvf = open(csv, 'r')
    csvflines = csvf.readlines()
    csvf.close()
    
    X = []
    Y = []
    
    for line in csvflines[1:]:
        freq, power, _ = line.split(',')
        X.append( int(freq) // 1000 )
        Y.append( float(power) )
        
    return X, Y


####################
### COMP AGENTES ###
####################

Xaa, Yaa = get_file_data('power_results/floatproduct.power.csv')
Xcc, Ycc = get_file_data('power_results/floatsum.power.csv')
Xdd, Ydd = get_file_data('power_results/floatsort.power.csv')

Xticks = np.arange(1200, 2700, 100)
Yticks = np.arange(35, 101, 5)

fig = plt.figure(figsize=(8,6), dpi=150)

ax = fig.add_subplot(111)

ax.plot(
    Xaa, Yaa, 
    color ='blue', 
    label = 'product',
    linestyle = '-',
    marker = 'o'
)

ax.plot(
    Xcc, Ycc, 
    color ='gold', 
    label = 'sum',
    linestyle = '-',
    marker = 'o'
)

ax.plot(
    Xdd, Ydd, 
    color ='green', 
    label = 'sort',
    linestyle = '-',
    marker = 'o'
)

ax.set_xlabel('Frequency (MHz)')
ax.set_xticks(Xticks)
ax.set_xticklabels(Xticks, rotation=45)

ax.set_ylabel('Power (W)')
ax.set_yticks(Yticks)

ax.grid(
    alpha=0.50,
    linestyle=':',
)
ax.legend(loc='upper left')

"""
ax.vlines(x=1600, ymin=35, ymax=52.5, color='r',linewidth=3.0, linestyle='--')
ax.hlines(y=52.5, xmin=1200, xmax=1600, color='r',linewidth=3.0,linestyle='--')
ax.plot(1600, 52.612215902606415, color = 'red', marker = 'o', markersize=12)

ax.text(1300, 55.0, '1600 MHz')
ax.text(1630, 45.0, '52.5 w')
"""


plt.savefig('7-1.png', bbox_inches='tight')