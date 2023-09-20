import matplotlib.pyplot as plt
import numpy as np
import sys


input_args = sys.argv[1:]
PROBLEM = input_args[0]
RUN = input_args[1]

# Mean
filename = f'tests/{PROBLEM}/mean.txt' 
with open(filename, 'r') as file:
    lines = file.readlines()
    values = [float(linha.strip()) for linha in lines]

values = np.array(values)

plt.plot(values)
plt.xlabel('Gerações')
plt.ylabel('Média')
plt.savefig(f'./tests/{PROBLEM}/mean_graph_run_{RUN}.png')
plt.close()

# Mean
filename = f'tests/{PROBLEM}/best_fit.txt' 
with open(filename, 'r') as file:
    lines = file.readlines()
    values = [float(linha.strip()) for linha in lines]

values = np.array(values)

plt.plot(values)
plt.xlabel('Gerações')
plt.ylabel('Melhor fit')
plt.savefig(f'./tests/{PROBLEM}/fit_graph_run_{RUN}.png')
plt.close()