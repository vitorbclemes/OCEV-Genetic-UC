import numpy as np
from genUtils import *
import time
import math

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
    COD,POP_SIZE,DIM,MUTATION,CROSSOVER,ELITISM,GEN,c = handle_file_input()
    # Generate initial population

    start_time = time.time()
    # Initial Pop
    population = generate_initial_population(POP_SIZE,DIM,COD)
    dinamic_mutation = MUTATION
    count = 0
    for i in range(GEN):
        fit_evaluate = []
        for individual in population:
            fit_evaluate.append(min_fitness(DIM,individual))
        #Eat elitism
        if(ELITISM > 0):
            best = population[fit_evaluate.index(max(fit_evaluate))]
        # Generate mid population
        selectedIndexes = rouletteSelection(fit_evaluate)
        mid_population = [population[k] for k in selectedIndexes]
        # Handle genetic operators
        new_generation = []
        for j in range(0,len(mid_population),2):
            if j+1< len(mid_population):
                if(np.random.rand() < CROSSOVER ):
                    a,b = pmx_crossover(mid_population[j],mid_population[j+1]) 
                    new_generation.append(a)
                    new_generation.append(b)
                else:
                    new_generation.append(mid_population[j])
                    new_generation.append(mid_population[j+1])
        # Handle mutation operators
        for j in range(len(new_generation)):
            if( np.random.rand() < dinamic_mutation ):
                new_generation[j] = swap_mutation(new_generation[j])

        # Vomit elitism
        if(ELITISM > 0):
            new_generation[np.random.randint(0,POP_SIZE)] = best


        population = new_generation

        new_generation_fit = []
        for individual in population:
            new_generation_fit.append(min_fitness(DIM,individual))
        # Handle dinamic mutation
        
        if((max(new_generation_fit) - np.mean(new_generation_fit)) < 0.01):
            dinamic_mutation += 0.01
        else:
            dinamic_mutation = MUTATION

        write_records(population,new_generation_fit,'nrainhas')

    end_time = time.time()
    elapsed_time = "{:.3f}".format(end_time - start_time)
    print(f"Elapsed time:{elapsed_time} seconds")

    with open(f'./tests/nrainhas/best_fit_end.txt',"a") as best_fit_end_file:
        best_fit_end_file.write(str(max(fit_evaluate)) + "\n")
    with open(f'./tests/nrainhas/best_mean_end.txt',"a") as best_mean_end_file:
        new_generation_fit = []
        for individual in population:
            new_generation_fit.append(min_fitness(DIM,individual))
        best_mean_end_file.write(str(np.mean(new_generation_fit)) + "\n")
    with open(f'./tests/nrainhas/time.txt',"a") as time_file:
        time_file.write(str(elapsed_time) + "\n")

