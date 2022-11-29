import math
import libraries as libs
import random
import numpy as np

def neighbor(solution):
    # Redistribute events
    events_grouped = libs.Functions.get_event_sublists(solution.config.ET)

    lcm = libs.Functions.lcm(solution.config.TT)
    for pt in solution.config.PT:
        # Mutate period
        pt.period = libs.Functions.get_polling_task_period(lcm, pt.period)

        # Mutate budget
        pt.budget = libs.Functions.get_polling_task_budget(solution.config.ET, pt.budget)

        # Set new events to PTs
        pt.assignedEvents = events_grouped[pt.separation]

    # return proposed solution
    return libs.Solution.schedule(solution.config)


# Peforms simulated annealing to find a solution
def simulated_annealing(initial_solution):
    initial_temp = 50
    final_temp = 1
    cooling_rate = 1

    current_temp = initial_temp

    # Start by initializing the current solution with the initial solution
    current_solution = initial_solution
    solution = current_solution

    while current_temp > final_temp:
        # Find a new neighbor solution
        proposed_solution = neighbor(current_solution)

        # Check if possible is better
        cost_diff = current_solution.cost - proposed_solution.cost

        # if the new solution is better, accept it
        if cost_diff > 0:
            solution = proposed_solution

        # if the proposed solution is not better, accept it with a probability of e^(-cost/temp)
        else:
            try:
                exp = np.exp(-cost_diff / current_temp)
            except:
                print('error calculating exp', '-cost_diff', cost_diff, 'current_temp', current_temp)
            if random.uniform(0, 1) < exp:
                solution = proposed_solution

        # cool the temperature
        current_temp -= cooling_rate

    return solution
