#!/usr/bin/env python3

import sys
import copy
import math
import libraries as libs

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# usage of addPollingTasks and usage 1
def schedule(csv):
    # Extract time triggered tasks from csv
    time_triggered_tasks = libs.CSVReader.get_tasks(csv, 'TT', False)
    if (len(time_triggered_tasks) <= 0):
        print(f"<{csv}> is empty or was not properly formed")
        exit(1)

    # Extract event triggered tasks from csv
    event_triggered_tasks = libs.CSVReader.get_tasks(csv, 'ET', False)
    if (len(event_triggered_tasks) <= 0):
        print(f"<{csv}> has no event triggered tasks")

    # Add time triggered polling tasks, if any
    time_triggered_tasks = libs.Polling.addTasks(time_triggered_tasks, event_triggered_tasks, 1)
    for tt in time_triggered_tasks:
        print(f'time_triggered_tasks: {str(tt.__dict__)}')

    # Get schedule table and worst-case response times
    #schedule, WCRT = libs.AlgoOne.schedulingTT(time_triggered_tasks)
    schedule, WCRT = libs.AlgoOne.schedulingTTPlot(time_triggered_tasks)

    #libs.Functions.printSchedule(schedule)
#    for time, T in enumerate(schedule):
#        print(f'time: {time} - {T.name} - {str(T.computation)}')

    return schedule, WCRT


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Ask user for file input
    csv = input("CSV path file: ") or 'resources/tasks.txt'

    # Init scheduling
    schedule(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
