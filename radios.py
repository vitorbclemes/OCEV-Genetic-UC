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
    COD,POP_SIZE,DIM,MUTATION,CROSSOVER,ELITISM,GEN,c = handle_file_input()

    start_time = time.time()
    # Initial Pop
    population = generate_initial_population(POP_SIZE,DIM,COD)
    dinamic_mutation = MUTATION
    for i in range(GEN):
        #Pop Fitness
        fit_evaluate = []
        for individual in population:
            fit_evaluate.append(fit_norm(individual))

        #Eat elitism
        if(ELITISM == 1):
            best = population[fit_evaluate.index(max(fit_evaluate))]

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
            new_generation[j] = bin_bitflip_mutation(new_generation[j],dinamic_mutation)

        # Vomit elitism
        if(ELITISM == 1):
            new_generation[np.random.randint(0,POP_SIZE)] = best

        # Update population
        population = new_generation

        new_generation_fit = []
        for individual in population:
            new_generation_fit.append(fit_norm(individual))

        # Handle dinamic mutation
        if(np.mean(new_generation_fit) - max(new_generation_fit) == 0):
            dinamic_mutation = 0.1
        else:
            dinamic_mutation = MUTATION


        write_records(population,new_generation_fit,'radios')

    end_time = time.time()
    elapsed_time = "{:.3f}".format(end_time - start_time)
    print(f"Elapsed time:{elapsed_time} seconds")

    with open(f'./tests/radios/best_fit_end.txt',"a") as best_fit_end_file:
        best_fit_end_file.write(str(max(fit_evaluate)) + "\n")
    with open(f'./tests/radios/best_mean_end.txt',"a") as best_mean_end_file:
        new_generation_fit = []
        for individual in population:
            new_generation_fit.append(fit_norm(individual))
        best_mean_end_file.write(str(np.mean(new_generation_fit)) + "\n")
    with open(f'./tests/radios/time.txt',"a") as time_file:
        time_file.write(str(elapsed_time) + "\n")