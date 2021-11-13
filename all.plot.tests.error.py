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

X = range(0, 201)

# Posición del dato a plotear
pos = 8 # power

# Valor objetivo del tipo de datos.
target = 52.5

# Color del plot
clr = 'blue'
targetclr = 'cyan'

# Ticks de los ejes.
Xticks = np.arange(0, 201, 10)
Yticks = np.arange(0, 46, 5)

# Figura 4x2
fig, axs = plt.subplots(
    4, 2, 
    figsize=(12,15), 
    dpi=150, 
    constrained_layout=True # ajusta bien los nombres del los ejes
    )

# Por cada época
for chkpt in range(8):
    # Gráfica de la grid
    ax = axs[chkpt // 2, chkpt % 2]

    # Título de la gráfica
    ax.set_title(f'Checkpoint {chkpt + 1}')

    # Por cada test (freq inicial)
    for it in range(15):
        data = get_file_data(f'checkpoint-{chkpt + 1}/iter-{it}.csv', pos)
        
        graph = []
        for value in data:
            graph.append( abs(value - target) )

        ax.plot(
            X, graph,
            color = clr,
            linestyle = '-',
            linewidth = 0.75,
            marker = '',
            alpha = 0.25
        )

    # Línea horizontal con el dato objetivo.
    ax.axhline(
        y = 0,
        xmin = 10 / 220,
        xmax = 1 - (10 / 220),
        color = targetclr,
        linestyle = '-',
        linewidth = 1.5
    )

    # Eje X.
    ax.set_xticks(Xticks)
    ax.set_xticklabels(Xticks, rotation = 45)

    # Eje Y.
    ax.set_yticks(Yticks)

    # Grid de la gráfica
    ax.grid(
        alpha = 0.25,
        linestyle = ':'
    )

# Texto de la figura 4x2
fig.text(0.5, -0.02, 'Número de paso', ha='center', va='center')
fig.text(-0.02, 0.5, 'Potencia (w)', ha='center', va='center', rotation='vertical')

# Ruta de guardado
plt.savefig('image.png', bbox_inches='tight')
