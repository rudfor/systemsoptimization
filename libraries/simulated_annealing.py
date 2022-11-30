import math
import libraries as libs
import random
import numpy as np

# Peforms simulated annealing to find a solution
def simulated_annealing(initial_solution, TT, ET):
    initial_temp = 14
    final_temp = 1
    cooling_rate = 2

    current_temp = initial_temp

    # Start by initializing the current solution with the initial solution
    current_solution = initial_solution
    solution = current_solution

    while current_temp > final_temp:
        # Find a new solution
        proposed_solution = libs.Solution.schedule(TT, ET)

        # Check if possible is better
        cost_diff = current_solution.cost - proposed_solution.cost

        # if the new solution is better, accept it
        if cost_diff > 0:
            solution = proposed_solution

        # if the proposed solution is not better, accept it with a probability of e^(-cost/temp)
        else:
            exp = np.exp(-cost_diff / current_temp)
            if random.uniform(0, 1) < exp:
                solution = proposed_solution

        # cool the temperature
        current_temp -= cooling_rate

    return solution
