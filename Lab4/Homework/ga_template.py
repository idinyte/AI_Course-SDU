import random
import queens_fitness

def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        ordered_population = list(population)
        weights = get_weights(ordered_population, fitness_fn)
        
        for i in range(max(0, min(len(population), 1000))): #clamp to a 1000
            mother, father = random_selection(ordered_population, weights)
            child_1, child_2 = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child_1 = mutate(child_1)
                
            if random.uniform(0, 1) < p_mutation:
                child_2 = mutate(child_2)

            print(child_1)
            new_population.add(child_1)
            new_population.add(child_2)
        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)
        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            print("Solution found!")
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''
    crossover_point = random.randrange(0,len(mother))
    child_1 = mother[:crossover_point] + father[crossover_point:]
    child_2 = father[:crossover_point] + mother[crossover_point:]
    return child_1, child_2


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    index = mutation_val = random.randrange(0,len(individual))
    while mutation_val == index:
        mutation_val = random.randrange(0,len(individual))
    mutation = list(individual)
    mutation[index] = mutation_val
    return tuple(mutation)

def get_weights(ordered_population, fitness_fn):
    '''
    Gets weights for random selection function. Gets them before for loop instead of every iteration.
    '''
    weights = list(map(lambda x: (MAXIMUM_FITNESS + fitness_fn(x)), ordered_population))
    ''' shifts the weights from [26, 27, 24] to [3, 4, 1] 
    min_w = min(weights)
    weights = list(map(lambda x: x - min_w + 1 , weights))
    '''
    return weights

def random_selection(ordered_population, weights):
    """
    Compute fitness of each in population according to fitness_fn and add up
    the total. Then choose 2 from sequence based on percentage contribution to
    total fitness of population
    Return selected variable which holds two individuals that were chosen as
    the mother and the father
    """
    parents = random.choices(ordered_population, weights=weights, k = 2)
    return parents[0], parents[1]
    ''' Also works, but slower
    fitnesses = MAXIMUM_FITNESS*len(ordered_population) + sum(map(fitness_fn, ordered_population))
    mother_fitness = random.randint(0, fitnesses)
    father_fitness = random.randint(0, fitnesses)
    sum_var = 0
    mother = 0
    father = 0
    for i in ordered_population:
        if mother != 0 and father != 0:
            break

        sum_var += MAXIMUM_FITNESS + fitness_fn(i) # 8 queen example: 28 + -2 
        if mother == 0 and sum_var >= mother_fitness: 
            mother = i
        if father == 0 and sum_var >= father_fitness:
            father = i 
    return mother, father
    '''
    


def fitness_function(individual):
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''
    return sum([j*2**i for i, j in enumerate(reversed(individual))])


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])

N_QUEENS = 8
MAXIMUM_FITNESS = N_QUEENS*(N_QUEENS - 1)/2

p_mutation = 0.1
num_of_generations = 15
population_size = 50

def main():
    minimal_fitness = 0
    queens_list = list(range(1, N_QUEENS + 1))
    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = set()
    for i in range(population_size):
        initial_population.add(tuple(random.sample(queens_list, N_QUEENS)))

    ''' placing queens randomly seems to find solution faster than the genetic algorithm
    rand_test = -1
    while rand_test != 0:
        rand = tuple(random.sample(queens_list, N_QUEENS))
        rand_test = queens_fitness.fitness_fn_negative(rand)
        print(rand)
    print('Fittest Individual: ' + str(rand) + ' fitness: ' + str(queens_fitness.fitness_fn_negative(rand)))
    '''

    ''' shows 27, when maximum is 28 and 2 queens conflict, so I don't trust this function
    #print(queens_fitness.fitness_fn_positive((1, 4, 7, 5, 0, 2, 6, 5))) 
    '''
    
    fittest = genetic_algorithm(initial_population, queens_fitness.fitness_fn_negative, minimal_fitness)
    print('Fittest Individual: ' + str(fittest) + ' fitness: ' + str(queens_fitness.fitness_fn_negative(fittest)))


if __name__ == '__main__':
    main()
