import random

# Параметры задачи
num_executors = 6  # Количество исполнителей
num_areas = 9      # Количество прикладных областей

# Коэффициенты эффективности исполнителей для каждой области
efficiency = [
    [0.035785097,   0.005908865,	0.006997008,	0.015952846,	0.039496238,	0.013181947,	8.90983E-05,	0.036407781,	0.0714702],
    [0.027260918,	0.020665346,	0.003269431,	0.008212968,	0.070361251,	0.015478999,	0.000730106,	0.016262221,	0.042548078],
    [0.044895105,	0.007651944,	0.021126886,	0.016926649,	0.142113763,	0.006538688,	0.000316496,	0.038656269,	0.023802077],
    [0.154102168,	0.019021657,	0.105804876,	0.00141518,	    0.133891915,	0.042078225,	0.005449941,	0.121265509,	0.259952718],
    [0.044548624,	0.024189201,	0.006570725,	0.006717459,	0.25747662,	    0.038673947,	0.003414497,	0.039284976,	0.091346571],
    [0.073342414,	0.045818569,	0.097412974,	0.032516724,	0.249764899,	0.012914872,	0.002959509,	0.137712934,	0.304094137]
]

# Задачи для каждой области (время выполнения)
tasks = [
    [15, 15, 15, 15, 10, 10, 20, 15, 15, 15, 10, 15, 20, 10, 10, 15],  # Задачи в области 0
    [60, 15, 15, 15, 15, 15, 15, 15, 120, 15, 15, 15, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 10, 10, 10, 10, 20, 5, 5, 5, 5, 5, 5, 15, 15, 15, 15, 15, 20, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],     # Задачи в области 1
    [10, 10, 10, 10, 10, 10],         # Задачи в области 2
    [15, 1440, 15, 15, 30, 10, 10, 10, 10, 10, 10, 10, 10, 60, 60, 60, 30, 30, 30, 30, 30, 30, 10, 10, 10, 10, 10, 10, 10, 120, 180, 120, 10, 120, 120, 120, 40, 10, 60, 60, 60, 10],
    [40, 45, 20, 35, 45, 35, 25, 35, 50, 45],
    [20, 30, 20, 40, 25, 20, 50, 50, 45, 45, 45, 45, 30, 20, 45, 25, 40, 35, 20, 20, 20, 20, 20, 50, 40, 50, 45, 30, 45, 20],
    [30, 25, 30, 40, 35, 25, 30, 20, 50, 30, 20, 40, 20, 35, 50, 50, 50, 30, 30, 50, 30, 45, 35, 25, 50, 40, 30, 50, 25, 25, 25, 30, 20, 45, 45, 35],
    [25, 25, 45, 20, 45, 20, 50, 20, 45, 30, 35, 25, 30, 35, 30],
    [35, 25, 50, 40, 40, 25, 40, 40, 45, 50, 50, 35, 30, 50, 35]
    # [150, 30, 30, 30, 30, 30] # 10
]

# Параметры генетического алгоритма
population_size = 10
num_generations = 50
mutation_rate = 0.1

def initialize_population():
    return [[random.randint(0, num_areas - 1) for _ in range(num_executors)] for _ in range(population_size)]

def calculate_schedule(individual):
    schedule = [[] for _ in range(num_executors)]
    task_times = [0] * num_areas
    
    for area, task_list in enumerate(tasks):
        for task in task_list:
            best_executor = None
            best_time = float('inf')
            
            for executor, assigned_area in enumerate(individual):
                if assigned_area == area:
                    start_time = task_times[area]
                    # end_time = start_time + task / efficiency[executor][area]
                    end_time = start_time + task

                    
                    if end_time < best_time:
                        best_executor = executor
                        best_time = end_time
            
            if best_executor is not None:
                schedule[best_executor].append((area, task_times[area], best_time))
                task_times[area] = best_time
    
    return schedule

def fitness(individual):
    schedule = calculate_schedule(individual)
    max_time = 0
    
    for executor_schedule in schedule:
        if executor_schedule:  # Проверяем, есть ли задачи у исполнителя
            executor_max_time = max(end_time for _, _, end_time in executor_schedule)
            max_time = max(max_time, executor_max_time)
    
    return max_time

def selection(population):
    population.sort(key=fitness)
    return population[:population_size // 2]

def crossover(parent1, parent2):
    point = random.randint(1, num_executors - 2)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual):
    if random.random() < mutation_rate:
        index = random.randint(0, num_executors - 1)
        individual[index] = random.randint(0, num_areas - 1)

def genetic_algorithm():
    population = initialize_population()
    
    for _ in range(num_generations):
        selected = selection(population)
        new_population = []
        
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected, 2)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        
        population = new_population
    
    best_solution = min(population, key=fitness)
    best_schedule = calculate_schedule(best_solution)
    
    return best_solution, fitness(best_solution), best_schedule

best_solution, best_fitness, best_schedule = genetic_algorithm()

print("Лучшее распределение:", best_solution)
print("Наименьшее максимальное время выполнения:", best_fitness)

for executor_index, tasks in enumerate(best_schedule):
    print(f"Исполнитель {executor_index}:")
    for area, start_time, end_time in tasks:
        print(f"  Область {area}: с {start_time:.2f} -> {end_time:.2f}")
