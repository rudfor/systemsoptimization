#!/usr/bin/env python3
import libraries as libs
import os
import sys
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
    print(f'intial BID:')
    #libs.Debug_Output.rudolf_test(initial_bid, args.plot)
    #libs.Solution.schedule(initial_bid,4)
    libs.Debug_Output.rudolf_test(initial_bid, args.plot)
    print(f'Debug OUtput:')

    # print(f'{testTask}')

    # START SEARCHING OF A SCHEDULE
    #solution = libs.Solution.search_solution2(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
