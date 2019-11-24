Self Oranizing Systems Exercise 1

The folders TSP and GC
each contain a python project which demonstrate the behaviour and performance of Genetic Algorithms (GA) and Ant Colony OptimizationA(ACO) on the given Problems.


### TSP
The main.py scripts can be executed without any further parameter.

The Lists in the beginning of the main script can be altered in order to execute various Problemsizes and set the number of GA-Iterations:
Please keep in mind the the elements of numberGenerations are mapped to the same index of problemsizeList

numberGenerations = [20, 275]
problemSizeList = [15, 30]
This exemplary set-up will cause that ACO and GA are executed for TSP problems with 15 and 30 cities. The GA optimization will be run for the 15 cities problem with 20 iterations and for 30 cities with 275 iterations..




### GRAPH COLOURING:

This project uses python 3.7, so you need to have it installed in order
to run the scripts.
You can find latest python releases here: https://www.python.org/downloads/


In order to install needed packages, run:

```bash
pip install -r requirements.txt
```

Everything is run from the main directory (Self-Organising_Systems_Exercise1_GraphColoring), so in order to run the scripts do:

```bash
$ EXPORT PYTHONPATH=.
$ python usecases/genetic_algorithms/genetic_algorithms.py -p graph_coloring -i 0010 -r 10
$ python usecases/ant_colony_optimizations/aco.py -p graph_coloring -i 0010 -r 10
```

This will run the graph_coloring on the instance 0010, and will repeat for 10 times. 


In order to try/add new parameters for GA, just modify the TESTING_PARAMETERS variable,
which looks something like this:

```
TESTING_PARAMETERS = [{
        'POPULATION_SIZE': 50,
        'NUMBER_OF_GENERATIONS': 200,
        'MUTATION_RATE': 0.05,
        'TOURNAMENT_SIZE': 10
    }]
```

Same setting is available for ACO-s as well, where parameters can be changed on:

```
TESTING_PARAMETERS = [{
        'ANT_COUNT': 200,
        'GENERATIONS': 100,
        'ALPHA': 0.5,
        'BETA': 8.0,
        'RHO': 0.5,
        'Q': 10,
        'STRATEGY': 1,
    }]
```


Running the script will save all results as xlsx files under `experiments` directory, with
the following naming convention (depending on what you run):

```
genetic_algorithm_graph_coloring_{current timestamp}.xlsx, or
aco_graph_coloring_{current timestamp}.xlsx
```

