#!/usr/bin/env python3
import libraries as libs
import os
import sys

from pprint import pformat
import maps
from immutables import Map

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = libs.Cli.cli()
    # allow user to add csv as argument else it will ask for input
    if args.csv is None:
        # Ask user for file input
        csv = input("CSV path file: ") or 'resources/tasks.txt'
    else:
        csv = args.csv

    hashseed = os.getenv('PYTHONHASHSEED')
    if not hashseed:
        os.environ['PYTHONHASHSEED'] = args.seed
        os.execv(sys.executable, [sys.executable] + sys.argv)

    #Initial Condition
    # Read CSV for Tasks
    TT, ET = libs.CSVReader.get_tasks_from_csv(csv)
    # Divide ET into Polling servers zeros are randomly placed
    sublistET = libs.PollingServer.get_event_sublists(ET, args.seed)
    print(f'LCM: TT: {libs.Functions.lcm(TT)}')
    for listET in sublistET:
        print(f'LCM: ET: PS_{listET}: {libs.Functions.lcm(sublistET[listET])}')

    for t in TT:
        print(f'{t}')
        print(f'Task Hash : {t.__hash__()}')

    PT = []
    for ps in sublistET:
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

    for t in PT:
        print(f'{t}')
        print(f'Task Hash : {t.__hash__()}')

    libs.AlgoOne.scheduling_TT(TT, visuals=True)
    libs.AlgoOne.scheduling_TT(PT, visuals=True)

    libs.AlgoOne.scheduling_TT(TT+PT, visuals=True)

    #libs.Solution.schedule(TT, PT)
    #print(f'{testTask}')
    #solution = libs.Solution.search_solution(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
