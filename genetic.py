import random

def generate_individual():
    return [random.randint(0, 7) for _ in range(8)]

def generate_population(size):
    return [generate_individual() for _ in range(size)]

def weighted_by(population):
    weightes = [fitness(ind) for ind in population]
    return weightes

def fitness(ind):
    conflicts = 0
    for i in range(len(ind)):
        for j in range(i+1, len(ind)):
            if ind[i] == ind[j] or abs(ind[i] - ind[j]) == abs(i - j):
                conflicts += 1
    return 1 / (1 + conflicts)

def weighted_random_choice(population, weights):
    sum_of_weightes = 0
    for w in weights:
        sum_of_weightes += w
    pick = random.uniform(0, sum_of_weightes)
    tmp = 0
    for i in range(len(weights)):
        tmp += weights[i]
        if tmp >= pick:
            return population[i]

def reproduce(parent1, parent2):
    c = random.randint(0, len(parent1)-1)
    return parent1[:c] + parent2[c:]

def mutate(child, mutation_rate):
    for i in range(len(child)):
        ran_num = random.random()
        if ran_num < mutation_rate:
            child[i] = random.randint(0, 7)

def genetic_algorithm(population_size, mutation_rate, max_generations):
    population = generate_population(population_size)
    for generation in range(max_generations):
        weights = weighted_by(population)
        population2 = []
        for _ in range(len(population)):
            parent1 = weighted_random_choice(population, weights)
            parent2 = weighted_random_choice(population, weights)
            child = reproduce(parent1, parent2)
            mutate(child, mutation_rate)
            population2.append(child)
        population = population2
        fit_ehough = max(population, key=fitness)
        if fitness(fit_ehough) == 1:
            return fit_ehough, generation
    print("Failed")
    fit_ehough = max(population, key=fitness)
    return fit_ehough, max_generations


def main():
    population_size = 100
    mutation_rate = 0.1
    max_generations = 1000

    solution, generations = genetic_algorithm(population_size, mutation_rate, max_generations)
    print("Solution:", solution)
    print("Generations:", generations)

if __name__ == "__main__":
    main()