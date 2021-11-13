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
Entornos: 1, 2, 3
Época: 5
Tests: 3 (cap:97.0)

Dato: potencia
Variable: entorno
Potencia objetivo: 97.0 W
"""

pos = 8 # power
X = range(0, 201)

# Parámetros de los datos.
envs = [1, 2, 3]
paths = [ f'./FinalEnv0{e}/' for e in envs ]
chkpt = 5

test_num = 3
tests = [ p + f'test-0{test_num}' for p in paths ]

target = 97.0
#################
# Etiquetas de cada plot.
label_tag = 'env'
labels = [ f'{label_tag}: {e}' for e in envs ]

# Color de cada plot.
clrs  = ['blue', 'aquamarine', 'lime']

# Ticks de los ejes.
maxY = 33
stepY = 2
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
plt.savefig('6-11.png', bbox_inches='tight')