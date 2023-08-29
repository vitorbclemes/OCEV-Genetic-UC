from genUtils import *
import sys

global c

def decode_bitArray_to_int(bitArray):
    bitString = ''.join(str(bit) for bit in bitArray)
    return int(bitString,2)

def f(st,lx):
    return 30*st + 40*lx

def fit_norm(individual):
    mid = len(individual) // 2
    st = round((decode_bitArray_to_int(individual[:mid]) * 24) / 31)
    lx = round((decode_bitArray_to_int(individual[mid:]) * 16) / 31)

    return (f(st,lx)/1360) +  c * max(0,(st + 2*lx - 40)/16) 

if __name__ == "__main__":
    POP_SIZE,DIM,COD = handle_file_input()
    c=-1

    initial_population = generate_initial_population(POP_SIZE,DIM,COD)
    
    fit_evaluate = []
    for individual in initial_population:
        fit_evaluate.append(fit_norm(individual))
    
    best_fit = max(fit_evaluate)
    worst_fit = min(fit_evaluate)

    print(f'Melhor individuo:{initial_population[fit_evaluate.index(best_fit)]}, FIT = {best_fit}')
    print(f'Pior individuo:{initial_population[fit_evaluate.index(worst_fit)]}, FIT = {worst_fit}')