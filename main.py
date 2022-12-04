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
    ET_schedulable, ET_WCRT = libs.PollingServer.check_polling_tasks_schedulability(initial_bid.PT)

    # Cost and result function
    # ALGO 1 (TT)
    # foreach PT
    # Algot 2 (ET)
    print(f'intial BID:')
    initial_bid.showPT()
    bid2 = initial_bid.get_neighbour()
    bid2.showPT()
    print(f'TT: {initial_bid.TT}\n\nPT: {initial_bid.PT}\n\nTT and PT:{initial_bid.TT + initial_bid.PT}\n\n')
    TT = initial_bid.TT + initial_bid.PT
    schedule1, wcrt1, data_frame1, isSchedulable1 = libs.AlgoOne.scheduling_TT(initial_bid.TT,
                                                                               visuals=False, return_df=True)
    data_frame1.plot(label='auto label', title='Time Triggered Tasks')

    schedule2, wcrt2, data_frame2, isSchedulable2 = libs.AlgoOne.scheduling_TT(initial_bid.PT,
                                                                               visuals=False, return_df=True)
    data_frame2.plot(label='auto label', title='Time Triggered Tasks')

    TT = initial_bid.TT + initial_bid.PT
    schedule3, wcrt3, data_frame3, isSchedulable3 = libs.AlgoOne.scheduling_TT(TT,
                                                                               visuals=False, return_df=True)
    data_frame3.plot(label='auto label', title='Time Triggered Tasks')

    bid3 = bid2.get_neighbour()

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    fig.suptitle('Horizontally stacked subplots')
    # data_frame1_diff = data_frame1.diff()
    # data_frame1.plot(ax=ax1, label='auto label', title='Time Triggered Tasks')
    data_frame1.plot(ax=ax1, label='auto label', title='Time Triggered Tasks')
    # ax1.set_yscale('log')
    plt.legend(ncol=3)

    # data_frame2_diff = data_frame2.diff()
    data_frame2.plot(ax=ax2, label='auto label', title='Polling Server ET Tasks')
    # ax2.set_yscale('log')
    plt.legend(ncol=3)

    data_frame3.plot(ax=ax3, label='auto label', title='Time Triggered and Polling Server')
    # ax3.set_yscale('log')
    plt.legend(ncol=3)
    plt.show()

    #libs.Debug_Output.rudolf_test(initial_bid, args.plot)
    #libs.Solution.schedule(initial_bid,4)
    #libs.Debug_Output.rudolf_test(initial_bid, args.plot)
    print(f'Debug Output:')

    # print(f'{testTask}')

    # START SEARCHING OF A SCHEDULE
    #solution = libs.Solution.search_solution2(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
