import random

# Project data: (cost, benefit)
projects = [
    (50000, 90000),  # Project 1
    (45000, 70000),  # Project 2
    (50000, 100000), # Project 3
    (30000, 60000),  # Project 4
    (45000, 85000),  # Project 5
    (40000, 80000),  # Project 6
    (30000, 50000)   # Project 7
]

# Parameters
budget = 200000
population_size = 10
iterations = 10
elitism_count = 2  # Number of top solutions to preserve
initial_mutation_rate = 0.2  # Start with a high mutation rate
final_mutation_rate = 0.05  # Reduce mutation rate as generations progress

# Fitness Function
def fitness(individual):
    total_cost = sum([projects[i][0] for i in range(len(individual)) if individual[i] == 1])
    total_benefit = sum([projects[i][1] for i in range(len(individual)) if individual[i] == 1])
    
    if total_cost <= budget:
        return total_benefit
    else:
        return 0

# Initial Population: Random binary chromosomes
def create_initial_population():
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, 1) for _ in range(len(projects))]
        population.append(individual)
    return population

# Selection: Roulette Wheel Selection
def selection(population):
    fitness_values = [fitness(ind) for ind in population]
    total_fitness = sum(fitness_values)
    
    if total_fitness == 0:
        return random.choice(population)  # Avoid division by zero if all solutions are invalid
    
    probabilities = [f / total_fitness for f in fitness_values]
    selected_indices = random.choices(range(len(population)), probabilities, k=2)
    
    return population[selected_indices[0]], population[selected_indices[1]]

# Crossover: Single-point crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2

# Mutation: Flip a random bit with a given mutation rate
def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

# Main genetic algorithm process
def genetic_algorithm():
    population = create_initial_population()
    print("Initial Population:")
    for ind in population:
        print(ind, "Fitness:", fitness(ind))
    
    for iteration in range(iterations):
        print(f"\nIteration {iteration + 1}:")
        
        # Calculate adaptive mutation rate
        mutation_rate = initial_mutation_rate - (iteration / iterations) * (initial_mutation_rate - final_mutation_rate)
        
        # Sort population by fitness in descending order
        population = sorted(population, key=fitness, reverse=True)
        
        # Preserve top individuals (elitism)
        new_population = population[:elitism_count]
        
        # Generate the rest of the new population using selection, crossover, and mutation
        while len(new_population) < population_size:
            parent1, parent2 = selection(population)
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.append(mutate(offspring1, mutation_rate))
            new_population.append(mutate(offspring2, mutation_rate))
        
        # Limit new population size to the desired number
        population = new_population[:population_size]
        
        # Output the best solution in the current population
        best_individual = max(population, key=fitness)
        print("Best Individual:", best_individual, "Fitness:", fitness(best_individual))
        
    return population

# Running the algorithm
final_population = genetic_algorithm()

# Show the final best solution
best_solution = max(final_population, key=fitness)
print("\nFinal Best Solution:", best_solution)
print("Total Benefit:", fitness(best_solution))
