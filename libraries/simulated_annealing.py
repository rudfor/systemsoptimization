import math
import libraries as libs
import random
import numpy as np

# Peforms simulated annealing to find a solution
def simulated_annealing(initial_solution, TT, ET):
    initial_temp = 50
    final_temp = 1
    cooling_rate = 2

    current_temp = initial_temp

    # Start by initializing the current solution with the initial solution
    current_solution = initial_solution
    solution = current_solution

    while current_temp > final_temp:
        neighbor = libs.Solution.schedule(TT, ET)

        # Check if neighbor is better
        cost_diff = current_solution.cost - neighbor.cost

        # if the new solution is better, accept it
        if cost_diff > 0:
            solution = neighbor

        # if the proposed solution is not better, accept it with a probability of e^(-cost/temp)
        else:
            exp = np.exp(-cost_diff / current_temp)
            if random.uniform(0, 1) < exp:
                solution = neighbor

        # cool the temperature
        current_temp -= cooling_rate

    return solution
