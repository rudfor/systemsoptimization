#!/usr/bin/env python3
import libraries as libs
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

    #Initial Condition
    # Read CSV for Tasks
    TT, ET = libs.CSVReader.get_tasks_from_csv(csv)
    # Divide ET into Polling servers zeros are randomly placed
    sublistET = libs.PollingServer.get_event_sublists(ET, args.seed)
    print(f'LCM: TT: {libs.Functions.lcm(TT)}')
    for listET in sublistET:
        print(f'LCM: ET: PS_{listET}: {libs.Functions.lcm(sublistET[listET])}')
    # Playing with HASHING
    if False:
        print(f'########################')
        hash_list = []
        for listET in sublistET:
            hash_list.append(hash(sublistET[listET].__repr__()))
            print(f'hash: {hash(sublistET[listET].__str__())}')
            print(f'list : {listET}{sublistET[listET]}')
            for taskET in sublistET[listET]:
                print(f'TASK: {hash(taskET)}')
        print(f'########################')
        print(f'{hash(pformat(sublistET))}')
        for hash_obj in hash_list:
            print(f'HS: {hash_obj}')

    for listET in sublistET:
        print(f'list : {listET}{sublistET[listET]}')


    # Init scheduling
    #solution = libs.Solution.search_solution(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
