#!/bin/bash
N=10

# Lê os valores do arquivo de entrada e remove os caracteres '\r'.
args=$(awk -F'=' '{gsub(/\r/,"",$2); print $2}' in)
args_array=($args)
PROBLEM="${args_array[-1]}"

echo "Problem:$PROBLEM"
rm -f tests/$PROBLEM/*
rm -f tests/$PROBLEM/*

for ((i=1; i<$N+1; i++))
do
    echo "------------"
    echo "Execução $i:"
    
    echo "Running solver..."

    # Chama o script Python com os argumentos.
    python3 $PROBLEM.py $args

    echo "Running graphs..."
    python3 results_interp.py $PROBLEM $i
    
    echo "Removing leftover files..."
    rm -f tests/$PROBLEM/best_fit.txt*
    rm -f tests/$PROBLEM/mean.txt*
    echo "Run $i done."
done

echo "DONE $N RUNS. Check tests/$PROBLEM/ for results"