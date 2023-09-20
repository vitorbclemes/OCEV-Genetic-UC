from genUtils import *
import time

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
    COD,POP_SIZE,DIM,MUTATION,CROSSOVER,GEN,c = handle_file_input()

    start_time = time.time()
    # Initial Pop
    population = generate_initial_population(POP_SIZE,DIM,COD)
    for i in range(GEN):
        #Pop Fitness
        fit_evaluate = []
        for individual in population:
            fit_evaluate.append(fit_norm(individual))
        # Generate mid population
        selectedIndexes = rouletteSelection(fit_evaluate)
        mid_population = [population[k] for k in selectedIndexes]

        # Handle genetic operators
        new_generation = []
        for j in range(0,len(mid_population),2):
            if j+1 < len(mid_population):
                if(np.random.rand() < CROSSOVER ):
                    a,b = bin_multipoint_crossover(mid_population[j],mid_population[j+1]) 
                    new_generation.append(a)
                    new_generation.append(b)
                else:
                    new_generation.append(mid_population[j])
                    new_generation.append(mid_population[j+1])
        # Handle mutation operators
        for j in range(len(new_generation)):
            new_generation[j] = bin_bitflip_mutation(new_generation[j],MUTATION)

        population = new_generation

        new_generation_fit = []
        for individual in population:
            new_generation_fit.append(fit_norm(individual))

        write_records(population,new_generation_fit,'radios')
    end_time = time.time()
    elapsed_time = "{:.3f}".format(end_time - start_time)
    print(f"Elapsed time:{elapsed_time} seconds")