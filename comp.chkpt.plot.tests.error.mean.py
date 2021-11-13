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

#paths = [ f'./FinalEnv0{i}/' for i in [1,2,3] ]
#tests = [ path + 'test-01' for path in paths ]

# Etiquetas de cada plot.
labels = [ f'env: {s}' for s in [1,2,3] ]

# Color de cada plot.
clrs = ['blue', 'cyan', 'midnightblue']
#clrs  = ['blue', 'aquamarine', 'lime']

# key = 'power' # sólo la usaba para el nombre del archivo de imagen

X = range(0, 201)

# Posición del dato a plotear
pos = 8 # power

# Valor objetivo del tipo de datos.
target = 52.5
#targetclr = 'black'

#targets = [52.5, 40.0, 97.0]

# Número de época.
chkpt = 5

# Ticks de los ejes.
Xticks = np.arange(0, 201, 10)
Yticks = np.arange(0, 18, 1)

# Figura
fig = plt.figure(figsize=(8,6), dpi=150)
ax = fig.add_subplot(111)


# Por cada agente.
for test, clr, label in zip(tests, clrs, labels):
    # Por cada test (freq inicial)
    bundle = []
    for it in range(15):
        data = get_file_data(
            test + f'/checkpoint-{chkpt}/iter-{it}.csv',
            pos
            )

        bundle.append( [ abs(x - target) for x in data ] )
    
    # Media de los tests.
    bundle = np.array(bundle)
    graph = bundle.mean(axis = 0)

    ax.plot(
        X, graph,
        color = clr,
        label = label,
        linestyle = '-',
        linewidth = 0.75,
        marker = '',
        alpha = 1.0
    )

# Línea horizontal con el dato objetivo.
""" ax.axhline(
    y = 0,
    xmin = 10 / 220,
    xmax = 1 - (10 / 220),
    color = targetclr,
    linestyle = '-',
    linewidth = 1.0
) """


# Eje X
ax.set_xlabel('Training step')
ax.set_xticks(Xticks)
ax.set_xticklabels(Xticks, rotation = 45)

# Eje Y
ax.set_ylabel('Average power error (W)')
ax.set_yticks(Yticks)

# Grid de la gráfica
ax.grid(
    alpha = 0.25,
    linestyle = ':'
)

# Leyenda
ax.legend()

# Ruta de guardado
plt.savefig('5-8.png', bbox_inches='tight')
