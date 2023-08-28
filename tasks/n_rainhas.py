import numpy as np
import sys
from tasks.genUtils import *


def min_fitness():
    # TO-DO
    pass

def max_fitness():
    # TO-DO
    pass

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

def store_best_and_worst_individuals(population):
    # Check for Collisions in each individual and store it
    classification_individuals = []
    for individual in population:
        classification_individuals.append(check_for_collisions(individual))

    # Check biggest and smallest collision numbers
    min_collisions = min(classification_individuals)
    max_collisions = max(classification_individuals)

    # List index(es) of min and max
    min_indices = [i for i, value in enumerate(classification_individuals) if value == min_collisions]
    max_indices = [i for i, value in enumerate(classification_individuals) if value == max_collisions]

    # Populate arrays with best and worst individuals
    min_individuals = [population[i] for i in min_indices]
    max_individuals = [population[i] for i in max_indices]

    return min_individuals,max_individuals


if __name__ == "__main__":
    # HANDLE ARGS FROM IN FILE
    input_args = sys.argv[1:]
    POP_SIZE = int(input_args[0])
    DIM = int(input_args[1])
    COD = str(input_args[2]).upper()

    # Generate initial population
    initial_population = generate_initial_population(POP_SIZE,DIM,COD)

    # Store best and worst individuals
    best,worst = store_best_and_worst_individuals(initial_population)
    print("Melhores individuos:",best)
    print("Piores individuos:",worst)

