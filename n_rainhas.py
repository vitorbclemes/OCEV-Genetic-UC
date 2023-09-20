import numpy as np
from genUtils import *

def check_for_collisions(individual):
    # Make a list of tuples with positions
    position_list = []
    for line,queen in enumerate(individual):
        position_list.append((line,queen))

    # Count the collisions
    colisions = 0
    for i,pos1 in enumerate(position_list):
        for pos2 in position_list[i+1:]:
            row_diff = abs(pos1[0] - pos2[0])
            col_diff = abs(pos1[1] - pos2[1])
            if(row_diff == col_diff):
                colisions+=1
    return colisions

def min_fitness(DIM,individual):
    max_colisions = sum(DIM-1 for _ in range(DIM))
    return (max_colisions - check_for_collisions(individual))/max_colisions

if __name__ == "__main__":
    POP_SIZE,DIM,COD = handle_file_input()
    # Generate initial population
    initial_population = generate_initial_population(POP_SIZE,DIM,COD)

    fit_evaluate = []
    for individual in initial_population:
        fit_evaluate.append(min_fitness(DIM,individual))

    best_fit = max(fit_evaluate)
    worst_fit = min(fit_evaluate)

    print(f'Melhor individuo:{initial_population[fit_evaluate.index(best_fit)]}, FIT = {best_fit}')
    print(f'Pior individuo:{initial_population[fit_evaluate.index(worst_fit)]}, FIT = {worst_fit}')


    