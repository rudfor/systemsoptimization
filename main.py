#!/usr/bin/env python3
import libraries as libs
import os
import sys
import copy
import pandas as pd
import matplotlib.pyplot as plt

# from pprint import pformat
# import maps
# from immutables import Map

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = libs.Cli.cli()
    # allow user to add csv as argument else it will ask for input
    if args.csv is None:
        # Ask user for file input
        csv = input("CSV path file: ") or "resources/test_case_with_separation.csv"
    else:
        csv = args.csv

    # TODO: Pass all bellow comments into the neighbor() in simulated_annealing.py
    #  and get_init_solution() in solution.py

    # Set Default Hashing to be
    hash_seed = os.getenv('PYTHONHASHSEED')
    if not hash_seed and args.seed != 999:
        os.environ['PYTHONHASHSEED'] = args.seed
        os.execv(sys.executable, [sys.executable] + sys.argv)

    verbosity = 4
    # Initial Condition
    # Read CSV for Tasks

    # TT, ET = libs.CSVReader.get_tasks_from_csv(csv)

    # Initial Condition
    initial_bid = libs.Bid(csv, args.seed, args.verbosity)
    solution, solutions = libs.Solution.search_solution_bid(initial_bid)
    solution.bid.plot(f'{csv.removeprefix("resources/testcases_orig2")}', True)

    #initial_bid.showPT()
    #print(f'initial solution: {initial_solution}')
    # Itterate 20 times
    if verbosity>9:
        current_bid = copy.deepcopy(initial_bid)

        for a in range(20):
            a = copy.deepcopy(current_bid.get_neighbour(5))
            current_bid = copy.deepcopy(a)
            next_bid_solution = libs.Solution.schedule_bid(a,5)
            print(f'initial solution: {next_bid_solution}')

        initial_bid.plot(f'{csv.removeprefix("resources/testcases_orig2")}', True)
        current_bid.plot(f'{csv.removeprefix("resources/testcases_orig2")} [Neighbour]', True)
        #next_bid.plot('NEXT', True)

        plt.show()

    #libs.Debug_Output.ruft_debug(initial_bid, args.plot)

    # START SEARCHING OF A SCHEDULE
    #solution = libs.Solution.search_solution2(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# RUN NOTES:
# ./main.py --csv resources/testcases_orig2/inf_10_10/taskset__1643188013-a_0.1-b_0.1-n_30-m_20-d_unif-p_2000-q_4000-g_1000-t_5__20__tsk.csv --seed 299 --verbosity 2 -p

