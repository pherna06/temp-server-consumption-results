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

def get_file_data(csv, pos):
    csvf = open(csv, 'r')
    csvflines = csvf.readlines()
    csvf.close()
    
    data = []    
    for line in csvflines[1:]:
        values =  line.strip('\n[]').split(',')
        data.append(float(values[pos]))

        # frecuencia en MHz:
        if pos == 7:
            data[-1] = data[-1] / 1000
        
    return data


####################
### COMP AGENTES ###
####################

# Ruta de los resultados del agente.
path = './FinalEnv01/'
tests = [ path + f'test-0{i}' for i in [1,4,5] ]

# Etiquetas de cada plot.
labels = [ f'size: {s}' for s in [3,2,4] ]

# Color de cada plot.
clrs = ['blue', 'cyan', 'midnightblue']

# key = 'power' # sólo la usaba para el nombre del archivo de imagen

X = [1,2,3]

# Posición del dato a plotear
pos = 8 # power

# Valor objetivo del tipo de datos.
target = 52.5
targetclr = 'black'

# Número de época.
chkpt = 5

# Ticks de los ejes.
# (se usa X) Xticks = np.arange(0, 201, 10)
Yticks = np.arange(0, 2.76, 0.25)

# Valor de X desde el que se empieza a contar
# (se descartan los valores del principio, cuando está convergiendo rápido)
count = 75

# Figura
fig = plt.figure(figsize=(4,4), dpi=150)
ax = fig.add_subplot(111)

# Por cada agente.
graph = []
for test in tests:
    bundle = []
    for it in range(15):
        data = get_file_data(
            test + f'/checkpoint-{chkpt}/iter-{it}.csv',
            pos
            )
        
        bundle.append( [ abs(x - target) for x in data ] )
    
    # Media sobre X (desde 'count')
    bundle = np.array(bundle)
    values = bundle.mean(axis = 0)
    graph.append( np.array( values[count:] ).mean() )


ax.bar(
    X, graph,
    color = clrs,
    linestyle = '-',
    width = 0.5,
    alpha = 1.0
)

# Eje X
ax.set_xticks(X)
ax.set_xticklabels(labels)

# Eje Y
ax.set_ylabel('Error medio acumulado')
ax.set_yticks(Yticks)

# Grid de la gráfica
ax.grid(
    alpha = 0.50,
    axis = 'y',
    linestyle = ':'
)

for index, value in enumerate(graph):
    plt.text(index + 0.87, value - 0.20, "{:.2f}".format(value), color = 'white')

# Ruta de guardado
plt.savefig('image.png', bbox_inches='tight')
