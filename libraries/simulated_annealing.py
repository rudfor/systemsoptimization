import math
import libraries as libs
import random
import numpy as np

def neighbor(solution):
    # Redistribute events
    events_grouped = libs.Functions.get_event_sublists(solution.config.ET)

    lcmTT = libs.Functions.lcm(solution.config.TT)
    lcmET = libs.Functions.lcm(solution.config.ET)

    # MUTATE THE PTs INSIDE THE CONFIG
    # config structure { TT, ET, PT }
    for pt in solution.config.PT:
        # Mutate period
        pt.period = libs.Functions.get_polling_task_period(lcmTT, lcmET, pt.period)

        # Mutate budget
        pt.budget = libs.Functions.get_polling_task_budget(solution.config.ET, pt.budget)

        # Mutate deadline
        pt.deadline = libs.Functions.get_pooling_task_deadline(events_grouped[pt.separation], pt.deadline)

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

    # SET CURRENT WITH INITIAL SOLUTION
    # Start by initializing the current solution with the initial solution
    current_solution = initial_solution
    solution = current_solution

    while current_temp > final_temp:
        # FIND NEIGHBOR SOLUTION
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
            # Add to Random DEBUG VERIFY
            if random.uniform(0, 1) < exp:
                solution = proposed_solution

        # cool the temperature
        current_temp -= cooling_rate

    # SA FINAL SOLUTION
    return solution
