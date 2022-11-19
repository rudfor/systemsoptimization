import math
import libraries as libs
import random

# Peforms simulated annealing to find a solution
def simulated_annealing(initial_solution, TT, ET):
    initial_temp = 90
    final_temp = .1
    alpha = 0.01

    current_temp = initial_temp

    # Start by initializing the current solution with the initial solution
    current_solution = initial_solution
    solution = current_solution

    while current_temp > final_temp:
        # neighbor = random.choice(get_neighbors())
        neighbor = libs.Solution.schedule(TT, ET)

        # Check if neighbor is best so far
        cost_diff = current_solution.cost - neighbor.cost

        # if the new solution is better, accept it
        if cost_diff > 0:
            solution = neighbor
        # if the new solution is not better, accept it with a probability of e^(-cost/temp)
        else:
            if random.uniform(0, 1) < math.exp(-cost_diff / current_temp):
                solution = neighbor

        # cool the temperature
        current_temp -= alpha

    return solution
