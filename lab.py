from genUtils import *
import numpy as np
import matplotlib.pyplot as plt
import time
import math


def f(st,lx):
    pass


def lab_reader(filename):
    lab = []
    with open(filename, 'r') as arquivo:
        lines = arquivo.readlines()
        for line in lines[1:-1]:
            line = line.strip()
            line = line.replace("{", "").replace("}", "")
            values = line.split(',')
            values = [int(value.strip()) for value in values if value.strip()]
            lab.append(values)
    return lab

def lab_plot(lab, way):
    fig, ax = plt.subplots()
    ax.matshow(lab, cmap='gray')

    caminho_x, caminho_y = zip(*way)
    ax.plot(caminho_y, caminho_x, 'r-', linewidth=2)

    ax.set_xticks([])
    ax.set_yticks([])

    plt.savefig("real/lab_final.png")

def getCrom(DIM):
    crom = [random.uniform(0, 0.9999) for _ in range(DIM)]
    return crom

def manhattan(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def move_validation(lab, pos, lab_copy):
    line, column = pos
    possible_moves = []

    for move in range(4):
        if move == 0:  # Baixo
            nova_line = line + 1
            new_column = column
        elif move == 1:  # Cima
            nova_line = line - 1
            new_column = column
        elif move == 2:  # Direita
            nova_line = line
            new_column = column + 1
        elif move == 3:  # Esquerda
            nova_line = line
            new_column = column - 1

        # Verificar se o move é válido e se a célula já foi visitada
        if (
            0 <= nova_line < len(lab)
            and 0 <= new_column < len(lab[0])
            and lab[nova_line][new_column] != 0
            and lab_copy[nova_line][new_column] != -1
        ):
            possible_moves.append(move)

    return possible_moves

def path_finder(crom, lab):
    first_line, first_column = 1, 1
    line, column = first_line, first_column

    lab_copy = [line.copy() for line in lab]
    path = [(line, column)]

    for value in crom:
        current_position = (line, column)
        possible_moves = move_validation(lab, current_position, lab_copy)

        if not possible_moves:
            break

        index = math.floor(len(possible_moves) * value)
        move = possible_moves[index]

        if move == 0:  # Down
            line += 1
        elif move == 1:  # Up
            line -= 1
        elif move == 2:  # Right
            column += 1
        elif move == 3:  # Left
            column -= 1

        path.append((line, column))
        lab_copy[line][column] = -1

    return path

def fitness(crom, lab, end_line, end_column):
    start_line, start_column = 1, 1
    line, column = start_line, start_column

    lab_copy = [line.copy() for line in lab]

    for value in crom:
        current_position = (line, column)
        possible_moves = move_validation(lab, current_position, lab_copy)

        if not possible_moves:
            break

        index = math.floor(len(possible_moves) * value)
        move = possible_moves[index]

        if move == 0:  # Down
            line += 1
        elif move == 1:  # Up
            line -= 1
        elif move == 2:  # Right
            column += 1
        elif move == 3:  # Left
            column -= 1

        # Marque a célula como visitada
        lab_copy[line][column] = -1

    distance = manhattan((line, column), (end_line, end_column))
    fitness = 1000 - distance

    return fitness

def probability(pop, lab, end_line, end_column):
    fitness_pop = [fitness(crom, lab, end_line, end_column) for crom in pop]
    fit_sum = sum(fitness_pop)
    probabilities = [fit/fit_sum for fit in fitness_pop]

    return probabilities

def roulette(pop, lab, end_line, end_column):
    probs = probability(pop, lab, end_line, end_column)

    roulette_instance = []
    for i, crom in enumerate(pop):
        roulette_instance.extend([crom] * int(probs[i] * 100))

    chosen = random.sample(roulette_instance, k=2)

    return chosen

if __name__ == "__main__":
    COD,POP_SIZE,DIM,MUTATION,CROSSOVER,ELITISM,GEN,c = handle_file_input()
    start_time = time.time()

    lab = lab_reader("./lab.txt")
    lab_copy = [line.copy() for line in lab]
    end_line, end_column = 23, 54

    # Initial Pop
    population = [getCrom(DIM) for _ in range(POP_SIZE)]
    mean_fitness_by_gen = []
    best_fitness_by_gen = []
    best_crom = None

    for i in range(GEN):
        current_best_crom = max(population,key=lambda crom:fitness(crom,lab,end_line,end_column))
        current_best_fitness = fitness(current_best_crom, lab, end_line, end_column)

        if best_crom is None or current_best_fitness > fitness(best_crom, lab, end_line, end_column):
            best_crom = current_best_crom

        selected_pairs = []
        while len(selected_pairs) < (POP_SIZE // 2):
            pair = roulette(population, lab, end_line, end_column)
            if pair[0] != pair[1]:
                selected_pairs.append(pair)
            
        new_children = []
        for pair in selected_pairs:
            child1, child2 = real_crossover(pair[0], pair[1], CROSSOVER, MUTATION)
            new_children.append(child1)
            new_children.append(child2)

        if current_best_fitness > max([fitness(crom, lab, end_line, end_column) for crom in new_children]):
            worst_child_index = [fitness(crom, lab, end_line, end_column) for crom in new_children].index(min([fitness(crom, lab, end_line, end_column) for crom in new_children]))
            new_children[worst_child_index] = current_best_crom

        pop_fitness = [fitness(crom, lab, end_line, end_column) for crom in population]
        mean_fitness = sum(pop_fitness) / len(population)
        mean_fitness_by_gen.append(mean_fitness)

        best_fit = max([fitness(crom, lab, end_line, end_column) for crom in population])
        best_fitness_by_gen.append(best_fit)

        population = new_children