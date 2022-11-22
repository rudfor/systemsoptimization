#!/usr/bin/env python3

import libraries as libs

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# CONSTANTS
ET = []
TT = []

def search_solution(csv):
    TT, ET = get_tasks_from_csv(csv)

    sep_counter = libs.Functions.count_separations(ET)

    # Get an initial solution to start the simulated annealing later
    initial_solution = libs.Solution.schedule(TT, ET)

    libs.Debug_Output.show_solution('Initial solution for TTs and TPs with ', initial_solution)

    solutions = []

    while len(solutions) < 5:
        print('Accepted solutions found so far: ', len(solutions))
        # Trigger simulated annealing
        proposed_solution = libs.simulated_annealing(initial_solution, TT, ET)

        libs.Debug_Output.show_solution('SA proposed solution for TTs and TPs with ', proposed_solution)

        # Validate solution is schedulable
        if not proposed_solution.schedulable:
            continue

        # Validate proposed_solution cost
        if proposed_solution.cost == 0:
            continue

        # Validate proposed_solution has right amount of PTs
        if proposed_solution.PT_created < sep_counter:
            continue

        solutions.append(proposed_solution)

    # Chose solution based on the min cost
    final_solution = libs.Solution.select_best_solution(solutions)

    libs.Functions.print_schedule(final_solution.schedule)

    return final_solution, solutions


def get_tasks_from_csv(csv):
    # Extract time triggered tasks from csv
    time_triggered_tasks = libs.CSVReader.get_tasks(csv, 'TT', False)
    if (len(time_triggered_tasks) <= 0):
        print(f"<{csv}> is empty or was not properly formed")
        exit(1)

    # Extract event triggered tasks from csv
    event_triggered_tasks = libs.CSVReader.get_tasks(csv, 'ET', False)
    if (len(event_triggered_tasks) <= 0):
        print(f"<{csv}> has no event triggered tasks")

    return time_triggered_tasks, event_triggered_tasks


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Ask user for file input
    csv = input("CSV path file: ") or 'resources/tasks.txt'

    # Init scheduling
    solution = search_solution(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
