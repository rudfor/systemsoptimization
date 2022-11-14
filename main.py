import sys
import copy
import math
import libraries as libs

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# usage of algorithm 2
def addPollingTasks(TT, ET, PTs = 1):
    # When no ET given, return TT as given
    if len(ET) < 1:
        return TT

    # Identify all given separations
    separations = []
    for task in ET:
        if task.separation not in separations:
            separations.append(task.separation)
    # Sort asc
    separations.sort()

    # For a given polling server, the search space for the period can be
    # between 2 and the hyperperiod of all TT tasks (2nd hint in pdf)
    lcm = libs.Functions.lcm(copy.deepcopy(TT))
    period = libs.Functions.getPollingTaskPeriod(lcm)
    print('Polling period:', period)

    # Add polling tasks for as many separations is requested
    while PTs > 0 and len(separations) > 0:
        # Find a separation which tasks can be schedulable
        foundSchedulableSeparation = False
        while not foundSchedulableSeparation and len(separations) > 0:
            bestBudget = 0
            worstResponseTime = 900000000

            # Get first available separation
            # 1
            separation = separations.pop(0)

            # Hill Climbing until found the best budget for polling task, if any
            attemptsDuringPlateau = 3
            for budget in range(1, period):
                # Get sublist of ET tasks with the same separation
                sublistET = []
                for task in ET:
                    # Fetch the ET tasks with current separation and with non-separation (zero)
                    if task.separation in [0, separation]:
                        sublistET.append(task)

                # Init the polling task attributes
                pollingTask = [budget, period, period]  # [budget, period, deadline = period]

                # Check if sublistET is schedulable
                schedulable, responseTime = libs.AlgoTwo.schedulingET(pollingTask[0], pollingTask[1], pollingTask[2], sublistET)

                # If separation is schedulable for budget then we store best responseTime and its budget.
                # Here we use response time as cost of our binary search in order to determine the best budget.
                if (schedulable == True and responseTime <= worstResponseTime):
                    worstResponseTime = responseTime
                    foundSchedulableSeparation = True

                    # Decrease attempts during plateau
                    if worstResponseTime == responseTime:
                        attemptsDuringPlateau -= 1

                    # Terminate search once consumed all plateau attempts
                    if attemptsDuringPlateau < 1:
                        break
                    bestBudget = budget

        if foundSchedulableSeparation:
            # Create polling task
            task.computation -=1
            task = libs.get_polling(separation, bestBudget, period, task)

            # Add polling task to Time Triggered tasks
            print('Add pooling schedulable task with separation:', separation, 'and budget:', bestBudget, 'and period:', period)
            TT.append(task)

            PTs -= 1

    return TT


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
    time_triggered_tasks = addPollingTasks(time_triggered_tasks, event_triggered_tasks, 1)

    # Get schedule table and worst-case response times
    schedule, WCRT = libs.AlgoOne.schedulingTT(time_triggered_tasks)

    libs.Functions.printSchedule(schedule)

    return schedule, WCRT


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Ask user for file input
    csv = input("CSV path file: ") or 'resources/tasks.txt'

    # Init scheduling
    schedule(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
