import math

# Funcao algébrica
def f(x):
    return math.cos(20*x) - (abs(x)/2) + (x**3/4)

# Funcao fitness para minimizar
def fit_min(x):
    return 2-f(x)

# Funcao fitness para maximizar
def fit_max(x):
    return f(x) - (-4)

# if __name__ == '__main__':
    # 14 bits, sendo 4 para parte inteira e 10 para parte fracionária