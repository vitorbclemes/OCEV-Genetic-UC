import sys
import numpy as np

# CONSTRAINTS
POP_SIZE = 10
DIM = 15

if __name__ == "__main__":
    # HANDLE ARGS FROM IN FILE
    input_args = sys.argv[1:]
    COD = str(input_args[0]).upper()

    if COD == 'BIN':
        initial_population = np.random.randint(2, size=(POP_SIZE, DIM))
    elif COD =='INT':
        initial_population = np.random.randint(-5,10,size=(POP_SIZE,DIM))
    elif COD == 'INT-PERM':
        initial_population = np.array([np.random.permutation(DIM) for _ in range(POP_SIZE)])
    elif COD == 'REAL':
        initial_population = np.random.uniform(-10,10,size=(POP_SIZE,DIM))
    else:
        print('Wrong input for COD arg')
    print(initial_population)