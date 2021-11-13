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
### 1 ÉPOCA ###
################

# Ruta de los resultados del agente.
path = './FinalEnv01/test-02/'

# key = 'power' # sólo la usaba para el nombre del archivo de imagen

X = range(0, 201)

# Posición del dato a plotear
pos = 8 # power

# Valor objetivo del tipo de datos.
target = 40.0

# Número de época.
chkpt = 5

# Color del plot
clr = 'blue'
targetclr = 'cyan'

# Ticks de los ejes.
Xticks = np.arange(0, 201, 10)
Yticks = np.arange(35, 101, 10)

# Figura
fig = plt.figure(figsize=(8,6), dpi=150)
ax = fig.add_subplot(111)

# Por cada test (freq inicial)
for it in range(15):
    data = get_file_data(
        path + f'checkpoint-{chkpt}/iter-{it}.csv', 
        pos
        )

    ax.plot(
        X, data,
        color = clr,
        linestyle = '-',
        linewidth = 0.75,
        marker = '',
        alpha = 0.25
    )

# Línea horizontal con el dato objetivo.
ax.axhline(
    y = target,
    xmin = 10 / 220,
    xmax = 1 - (10 / 220),
    color = targetclr,
    linestyle = '-',
    linewidth = 1.0
)

# Eje X
ax.set_xlabel('Número de paso')
ax.set_xticks(Xticks)
ax.set_xticklabels(Xticks, rotation = 45)

# Eje Y
ax.set_ylabel('Potencia (w)')
ax.set_yticks(Yticks)

# Grid de la gráfica
ax.grid(
    alpha = 0.25,
    linestyle = '-'
)

# Ruta de guardado
plt.savefig('image.png', bbox_inches='tight')
