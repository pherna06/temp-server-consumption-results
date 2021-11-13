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


################
### 8 ÉPOCAS ###
################

# key = 'power' # sólo la usaba para el nombre del archivo de imagen

X = range(1, 9) # 8 épocas

# Posición del dato a plotear
pos = 8 # power

# Valor objetivo del tipo de datos.
target = 52.5

# Color del plot
clr = 'blue'
targetclr = 'cyan'

# Ticks de los ejes.
# (no se usan) Xticks = np.arange(0, 201, 10)
Yticks = np.arange(0, 6, 0.5)

# Valor de X desde el que se empieza a contar
# (se descartan los valores del principio, cuando está convergiendo rápido)
count = 75

# Por cada época
graph = []
for chkpt in range(8):
    bundle = []

    # Por cada test (freq inicial)
    for it in range(15):
        data = get_file_data(f'checkpoint-{chkpt + 1}/iter-{it}.csv', pos)
        bundle.append( [ abs(x - target) for x in data ] )

    # Media sobre X (desde 'count')
    bundle = np.array(bundle)
    values = bundle.mean(axis = 0)
    graph.append( np.array( values[count:] ).mean() )

fig = plt.figure(figsize=(12,9), dpi=150)
ax = fig.add_subplot(111)

ax.bar(
    X, graph,
    color = clr,
    linestyle = '-',
    width = 0.5,
    alpha = 1.0
)

Xlabels = [f'chkpt-{x}' for x in X]
ax.set_xticks(X)
ax.set_xticklabels(Xlabels, rotation = 45)

ax.set_ylabel('Error medio acumulado')
ax.set_yticks(Yticks)
       
# Grid de la gráfica
ax.grid(
    alpha = 0.50,
    axis = 'y',
    linestyle = ':'
)

# Valores mostrados en barras.
for index, value in enumerate(graph):
    # Normalmente hay que cambiar los desplazamientos para cada tipo de datos.
    plt.text(index + 0.86, value - 0.2, "{:.2f}".format(value), color = 'white')

# Ruta de guardado
plt.savefig('image.png', bbox_inches='tight')
