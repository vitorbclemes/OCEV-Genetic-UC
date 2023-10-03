import matplotlib.pyplot as plt
import numpy as np
import sys

input_args = sys.argv[1:]
PROBLEM = input_args[0]

# Best Fit Boxplot
filename = f'tests/{PROBLEM}/best_fit_end.txt' 
with open(filename, 'r') as file:
    lines = file.readlines()
    values = [float(linha.strip()) for linha in lines]

values = np.array(values)

plt.boxplot(values)
plt.xlabel('Fitness')
plt.ylabel('Execuções')
plt.title('Melhor fitness')
plt.savefig(f'./tests/{PROBLEM}/best_fit_end_graph.png')
plt.close()


# Time Boxplot
filename = f'tests/{PROBLEM}/time.txt'
with open(filename, 'r') as file:
    lines = file.readlines()
    values = [float(linha.strip()) for linha in lines]

values = np.array(values)

plt.boxplot(values)
plt.xlabel('Tempo(s)')
plt.ylabel('Execuções')
plt.title('Tempo de execução')
plt.savefig(f'./tests/{PROBLEM}/time_graph.png')
plt.close()