#!/usr/bin/env python3
import libraries as libs
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

from pprint import pformat
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


    # hashseed = os.getenv('PYTHONHASHSEED')
    # if not hashseed:
    #     os.environ['PYTHONHASHSEED'] = args.seed
    #     os.execv(sys.executable, [sys.executable] + sys.argv)

    verbosity = 3
    #Initial Condition
    # Read CSV for Tasks

    TT, ET = libs.CSVReader.get_tasks_from_csv(csv)

    # Divide ET into Polling servers zeros are randomly placed
    # sublistET = libs.PollingServer.get_event_sublists(ET, args.seed)
    # print(f'LCM: TT: {libs.Functions.lcm(TT)}')
    # for listET in sublistET:
    #     print(f'LCM: ET: PS_{listET}: {libs.Functions.lcm(sublistET[listET])}')
    #
    # for t in TT:
    #     print(f'{t}')
    #     print(f'Task Hash : {t.__hash__()}')

<<<<<<< HEAD
    # PT = []
    # for ps in sublistET:
    #     testTask = libs.TaskModel(name=f'PT{ps}',
    #                               computation=libs.Functions.computation(sublistET[ps]),
    #                               period=libs.Functions.lcm(sublistET[ps]),
    #                               priority=7,
    #                               type='PT',
    #                               deadline=libs.Functions.deadline(sublistET[ps]),
    #                               separation=ps,
    #                               assigned_events=(sublistET[ps])
    #                               )
    #     PT.append(testTask)

    # for t in PT:
    #     print(f'{t}')
    #     print(f'Task Hash : {t.__hash__()}')

    # schedule1, wcrt1, isSchedulable1 = libs.AlgoOne.scheduling_TT(TT, visuals=args.plot)
    # schedule2, wcrt2, isSchedulable2 = libs.AlgoOne.scheduling_TT(PT, visuals=args.plot)
    #
    # schedule3, wcrt3, isSchedulable3 = libs.AlgoOne.scheduling_TT(TT+PT, visuals=args.plot)

    # print(f'wcrt: {wcrt1}, schedulable={isSchedulable1}')
    # print(f'wcrt: {wcrt2}, schedulable={isSchedulable2}')
    # print(f'wcrt: {wcrt3}, schedulable={isSchedulable3}')
=======
    if (verbosity > 3):
        for t in TT:
            print(f'{t}')
            if (verbosity > 4): print(f'Task Hash : {t.__hash__()}')

    PT = []
    for ps in sublistET:
        # Create a new Polling Task Server using a group of ET tasks
        testTask = libs.TaskModel(name=f'PT{ps}',
                                  computation=libs.Functions.computation(sublistET[ps]),
                                  period=libs.Functions.lcm(sublistET[ps]),
                                  priority=7,
                                  type='PT',
                                  deadline=libs.Functions.deadline(sublistET[ps]),
                                  separation=ps,
                                  assigned_events=(sublistET[ps])
                                  )
        PT.append(testTask)

    if (verbosity > 3):
        for t in PT:
            print(f'{t}')
            print(f'Task Hash : {t.__hash__()}')
    # SCHEDULE
    schedule1, wcrt1, data_frame1, isSchedulable1 = libs.AlgoOne.scheduling_TT(TT, visuals=args.plot, return_df=True)
    schedule2, wcrt2, data_frame2, isSchedulable2 = libs.AlgoOne.scheduling_TT(PT, visuals=args.plot, return_df=True)

    schedule3, wcrt3, data_frame3, isSchedulable3 = libs.AlgoOne.scheduling_TT(TT+PT, visuals=args.plot, return_df=True)

    if args.plot:
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        fig.suptitle('Horizontally stacked subplots')
        data_frame1_diff = data_frame1.diff()
        data_frame1_diff.plot(ax=ax1, label='auto label', title='Time Triggered Tasks')
        #ax1.set_yscale('log')
        plt.legend(ncol=3)
        data_frame2_diff = data_frame2.diff()
        data_frame2_diff.plot(ax=ax2, label='auto label', title='Polling Server ET Tasks')
        #ax2.set_yscale('log')
        plt.legend(ncol=3)
        data_frame3.plot(ax=ax3, label='auto label', title='Time Triggered and Polling Server')
        #ax3.set_yscale('log')
        plt.legend(ncol=3)
        plt.show()
        #fig, (ax1, ax2) = plt.subplots(1, 2)

    print(f'wcrt: {wcrt1}, schedulable={isSchedulable1}')
    print(f'wcrt: {wcrt2}, schedulable={isSchedulable2}')
    print(f'wcrt: {wcrt3}, schedulable={isSchedulable3}')
>>>>>>> 884a0c1 (fix display and schedule one)

    #libs.Solution.schedule(TT, PT)
    #print(f'{testTask}')

    # START SEARCHING OF A SCHEDULE
    solution = libs.Solution.search_solution(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
