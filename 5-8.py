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

"""
Entorno: 1
Época: 5
Tests: 1 (size:3), 4 (size:2), 5 (size:4)

Dato: potencia
Variable: tamaño de intervalo
Potencia objetivo: 52.5 W
"""

pos = 8 # power
X = range(0, 201)

# Parámetros de los datos.
path = './FinalEnv01/'
chkpt = 5

test_nums = [1, 4, 5]
tests = [ path + f'test-0{i}' for i in test_nums ]

target = 52.5
#################

# Etiquetas de cada plot.
label_tag = 'size'
sizes = [3, 2, 4]
labels = [ f'{label_tag}: {s}' for s in sizes ]

# Color de cada plot.
clrs = ['blue', 'cyan', 'midnightblue']

# Ticks de los ejes.
maxY = 18
stepY = 1
Xticks = np.arange(0, 201, 10)
Yticks = np.arange(0, maxY, stepY)

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
ax.set_xlabel('Time (inference step)')
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
