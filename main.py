import sys
import re
import os
import libraries as libs

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def schedule(triggered_task, event_task, time_limit=10000):
    """
    TT = Time Triggered
    ET = Event Triggerd
         Sporadic
    EDF = Earliest Deadline First
    RM = Rate Monotonic
    WCET = Worst Case Execution Time
    pi => task priority
    Di => relative deadline
    Ci => Compution time
    TT => Ti Period
    EF => Ti Sporadic
    :param T:
    :return:
    """
    TT = triggered_task
    t = 0
    schedule = [0] * time_limit
    # We go through each slot in the schedule table until T (time_limit)
    while t <= time_limit:
        wcrt = []
        #for t in range(time_limit,1): # while t < T do
        print(f"EDF: {TT.edf()}")
        for T in TT.tasks:
            print(f"{T.name}")
            if T.duration > 0 and T.deadline <= t:
                libs.Debug_Output.message(f"Deadline Missed", t, T)
                sys.exit(1)
            if T.duration == 0 and T.deadline >= t:
                if (t - T.r) >= T.wcrt:
                    T.wcrt = (t - T.r)
                    wcrt.append(T.wcrt)
                libs.Debug_Output.message(f"Check if the current WCRT is larger than the current maximum", t, T, True)
            if t % T.period == 0:
                T.r = t
                T.duration = T.init_duration
                T.deadline = T.init_deadline + t
        idle = True
        for T in TT.tasks:
            if T.duration > 0:
                print(f"Time at Idle: {t}")
                #schedule[t]='idle'
                idle = False
            else:
                pass
        if not idle:
            Ti = None
            # Run time TI to pass by reference.
            for T in TT.tasks:
                if Ti == None:
                    Ti = T
                elif T.deadline < Ti.deadline:
                    Ti = T
            schedule[t]=Ti
            Ti.duration -=1


        t += 5

        print(f"{wcrt}")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    triggered_task = libs.Tasks('resources/tasks.txt','TT')
    print(f"{triggered_task}")
    #event_task = libs.ReadTasks.get_tasks('resources/tasks.txt','ET')
    event_task = []

    schedule(triggered_task, event_task)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
