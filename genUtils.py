import numpy as np
import sys
import random
import os

BASH_SCRIPT_PID = 0
# Handle parameters interpretation from in file and return them
def handle_file_input():
    # HANDLE ARGS FROM IN FILE
    input_args = sys.argv[1:]
    COD = str(input_args[0]).upper()
    POP_SIZE = int(input_args[1])
    DIM = int(input_args[2])
    MUTATION = float(input_args[3])
    CROSSOVER = float(input_args[4])
    ELITISM = int(input_args[5])
    GEN = int(input_args[6])
    c = float(input_args[7])
    BASH_SCRIPT_PID = int(input_args[9])

    return COD,POP_SIZE,DIM,MUTATION,CROSSOVER,ELITISM,GEN,c

# Generates initial population based on parameters
def generate_initial_population(POP_SIZE,DIM,COD):
    if COD == 'BIN':
        initial_population = np.random.randint(2, size=(POP_SIZE, DIM))
    elif COD =='INT':
        initial_population = np.random.randint(-5,10,size=(POP_SIZE,DIM))
    elif COD == 'INT-PERM':
        initial_population = np.array([np.random.permutation(DIM) for _ in range(POP_SIZE)])
    elif COD == 'REAL':
        initial_population = np.random.uniform(-10,10,size=(POP_SIZE,DIM))
    else:
        print(f'Wrong input for COD arg')
        os.kill(BASH_SCRIPT_PID, 15) 
    return initial_population

# Returns the relative fitness for the population
def relative_fit(fit_evaluate):
    sum_fit = sum(fit for fit in fit_evaluate)
    relative_fit_array = [fit/sum_fit for fit in fit_evaluate]
    return relative_fit_array

def rouletteSelection(fit_evaluate):
    rouletteOptions = relative_fit(fit_evaluate)
    roulettePairs = []

    for _ in range(int(len(fit_evaluate) / 2)):
        rouletteOptionsCopy = rouletteOptions.copy()
        selected_indices = []

        for __ in range(2):
            limit = np.random.uniform(0, 1)
            limitSum = 0

            for i in range(len(rouletteOptionsCopy)):
                if limit <= rouletteOptionsCopy[i] + limitSum:
                    selected_indices.append(i)
                    break
                else:
                    limitSum += rouletteOptionsCopy[i]

        roulettePairs.extend(selected_indices)

    return roulettePairs


def bin_onepoint_crossover(parent_a,parent_b,sliceIndex = None):
    if(sliceIndex == None):
        parentSize = len(parent_a)
        sliceIndex = np.random.randint(0,parentSize)
    new_parent_a = np.append(parent_a[:sliceIndex],parent_b[sliceIndex:])
    new_parent_b = np.append(parent_b[:sliceIndex],parent_a[sliceIndex:])
    return new_parent_a, new_parent_b

def bin_multipoint_crossover(parent_a,parent_b):
    parentSize = len(parent_a)
    sliceIndexes = [np.random.randint(0,parentSize),np.random.randint(0,parentSize)]
    for index in sliceIndexes:
        new_parent_a,new_parent_b = bin_onepoint_crossover(parent_a,parent_b,index)
    return new_parent_a,new_parent_b

def bin_uniform_crossover(parent_a,parent_b):
    parentSize = len(parent_a)
    P = np.random.rand(parentSize)
    for i in range(len(P)):
        if P[i] < 0.5:
            temp = parent_a[i]
            parent_a[i] = parent_b[i]
            parent_b[i] = temp
    return parent_a,parent_b

def bin_bitflip_mutation(individual,mutation_rate):
    for i in range(len(individual)):
        if(np.random.rand() < mutation_rate):
            individual[i] = 1 if individual[i] == 0 else 1
    return individual

def pmx_crossover(parent1, parent2):
    cutoff_1, cutoff_2 = np.sort(np.random.choice(np.arange(len(parent1)+1), size=2, replace=False))

    def PMX_one_offspring(p1, p2):
        offspring = np.zeros(len(p1), dtype=p1.dtype)

        # Copy the mapping section (middle) from parent1
        offspring[cutoff_1:cutoff_2] = p1[cutoff_1:cutoff_2]

        # copy the rest from parent2 (provided it's not already there
        for i in np.concatenate([np.arange(0,cutoff_1), np.arange(cutoff_2,len(p1))]):
            candidate = p2[i]
            while candidate in p1[cutoff_1:cutoff_2]: # allows for several successive mappings
                candidate = p2[np.where(p1 == candidate)[0][0]]
            offspring[i] = candidate
        return offspring

    offspring1 = PMX_one_offspring(parent1, parent2)
    offspring2 = PMX_one_offspring(parent2, parent1)
    return offspring1, offspring2

def swap_mutation(individual):
    size = len(individual)
    mutated_individual = individual.copy()

    # Escolhe duas posições aleatórias diferentes para trocar
    position1, position2 = random.sample(range(size), 2)

    # Realiza a troca
    mutated_individual[position1], mutated_individual[position2] = mutated_individual[position2], mutated_individual[position1]

    return mutated_individual


def write_records(population,population_fit,problem_label):
    with open(f'./tests/{problem_label}/mean.txt',"a") as mean_file:
        mean_file.write(str(np.mean(population_fit)) + "\n")
    with open(f'./tests/{problem_label}/best_fit.txt',"a") as best_fit_file:
        best_fit_file.write(str(max(population_fit)) + "\n")
    # with open(f'./tests/{problem_label}/best_individual.txt',"a") as best_individual_file:
    #     best_indiv_index = population_fit.index(max(population_fit))
    #     best_individual_file.write(population[best_indiv_index])

    mean_file.close()
    best_fit_file.close()
    # best_individual_file.close()