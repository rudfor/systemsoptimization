import sys
import copy
import libraries as libs
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np


class AlgoOne:
    """
    # algorithm 1
    """
    @staticmethod
    def schedulingTT(TT, time_limit=10000):
        """
        Data: TT task set TT T including polling server tasks T poll
        Result: TT schedule table (σ) and WCRTs of TT tasks (W CRTi)

        TT = Time Triggered
        EDF = Earliest Deadline First
        RM = Rate Monotonic
        WCET = Worst Case Execution Time
        pi => task priority
        Di => relative deadline
        Ci => Compution time (duration)
        TT => Ti Period
        EF => Ti Sporadic
        :param T:
        :return:
        """
        # Get least common multiple of task priorities
        time_limit = libs.Functions.lcm(copy.deepcopy(TT)) or time_limit
        print(f"TT lcm: ", time_limit)

        # Start time
        t = 0

        # Init schedule table
        schedule = [0] * time_limit

        # We go through each time slot in until we reach the time limit
        watchDog = 50000
        while t < time_limit:
            # print(f"EDF: {libs.Functions.edf(t, TT.tasks).name}")
            for T in TT:
                # print(f"{T.name}")

                # Check time has not passed task deadline
                if T.computation > 0 and T.deadline <= t:
                    libs.Debug_Output.message(f"Deadline Missed", t, T)
                    sys.exit(1)

                # Check time is behind task deadline
                if T.computation == 0 and T.deadline >= t:
                    # Check wcrt is the maximum response time over all T jobs
                    # libs.Debug_Output.message(f"Check if the current WCRT {t - T.r} is larger than the current maximum {T.wcrt}", t, T)
                    if (t - T.r) >= T.wcrt:
                        # Update max
                        T.wcrt = t - T.r

                # When task is completed we should reset its duration and move deadline to the present
                if t % T.period == 0:
                    T.r = t
                    T.computation = T.init_computation
                    T.deadline = T.init_deadline + t
                    print('reset on period', T.name, T.computation, T.init_deadline, T.deadline, t)

            # Check if there is any tasks with computation left
            if all(task.computation == 0 for task in TT):
                # If no task has computation left, schedule idle slot
                schedule[t] = libs.get_idle()
            else:
                # Get task with earliest deadline
                ti = libs.Functions.edf(TT, t)

                # Add task to the current second in the schedule
                # print(f"add to schedule {ti.name} at {t}")
                schedule[t] = copy.deepcopy(ti)

                # Since we execute the task in the current second then we
                # reduce by one time second the remaining duration of the task
                ti.computation -= 1

            # Tick the clock
            t += 1

            if watchDog < 0:
                print('Force break triggered of scheduling of TT tasks...')
                break
            watchDog -= 1

        # If at least one task has its duration more than 0 that indicates
        # that at least one task is not completed and therefore the schedule
        # is infeasible for the given combination of tasks in the given time limit.
        if any(task.computation > 0 for task in TT):
            for T in TT:
                libs.Debug_Output.message(f"Schedule is infeasible if any TT task has ci > 0 at this point", t, T)
            sys.exit(1)

        # print(f"{schedule}")
        wcrt = [task.wcrt for task in TT]
        # print(wcrt)

        return schedule, wcrt

    @staticmethod
    def schedulingTTPlot(TT, time_limit=10000):
        """
        Data: TT task set TT T including polling server tasks T poll
        Result: TT schedule table (σ) and WCRTs of TT tasks (W CRTi)

        TT = Time Triggered
        EDF = Earliest Deadline First
        RM = Rate Monotonic
        WCET = Worst Case Execution Time
        pi => task priority
        Di => relative deadline
        Ci => Compution time (duration)
        TT => Ti Period
        EF => Ti Sporadic
        :param T:
        :return:
        """
        # Get least common multiple of task priorities
        time_limit = libs.Functions.lcm(copy.deepcopy(TT)) or time_limit
        print(f"TT lcm: ", time_limit)
        csv_header = ""
        for T in TT:
            if csv_header:
                csv_header = f'{csv_header}, {T.name}'
            else:
                csv_header = f'{T.name}'

        # Start time
        t = 0

        # Init schedule table
        schedule = [0] * time_limit

        # We go through each time slot in until we reach the time limit
        watchDog = 50000
        csv_content = []
        while t < time_limit:
            csv_line = ''
            # print(f"EDF: {libs.Functions.edf(t, TT.tasks).name}")
            for T in TT:
                # print(f"{T.name}")

                # Check time has not passed task deadline
                if T.computation > 0 and T.deadline <= t:
                    libs.Debug_Output.message(f"Deadline Missed", t, T)
                    sys.exit(1)

                # Check time is behind task deadline
                if T.computation == 0 and T.deadline >= t:
                    # Check wcrt is the maximum response time over all T jobs
                    # libs.Debug_Output.message(f"Check if the current WCRT {t - T.r} is larger than the current maximum {T.wcrt}", t, T)
                    if (t - T.r) >= T.wcrt:
                        # Update max
                        T.wcrt = t - T.r

                # When task is completed we should reset its duration and move deadline to the present
                if t % T.period == 0:
                    T.r = t
                    T.computation = T.init_computation
                    T.deadline = T.init_deadline + t
                    print('reset on period', T.name, T.computation, T.init_deadline, T.deadline, t)

                if csv_line:
                    csv_line = f'{csv_line}, {T.computation}'
                else:
                    csv_line = f'{T.computation}'

            #print(f'csv_line: {csv_line}')
            csv_content.append(csv_line)

            # Check if there is any tasks with computation left
            if all(task.computation == 0 for task in TT):
                # If no task has computation left, schedule idle slot
                schedule[t] = libs.get_idle()
            else:
                # Get task with earliest deadline
                ti = libs.Functions.edf(TT, t)

                # Add task to the current second in the schedule
                # print(f"add to schedule {ti.name} at {t}")
                schedule[t] = copy.deepcopy(ti)

                # Since we execute the task in the current second then we
                # reduce by one time second the remaining duration of the task
                ti.computation -= 1

            # Tick the clock
            t += 1

            if watchDog < 0:
                print('Force break triggered of scheduling of TT tasks...')
                break
            watchDog -= 1

        # If at least one task has its duration more than 0 that indicates
        # that at least one task is not completed and therefore the schedule
        # is infeasible for the given combination of tasks in the given time limit.
        if any(task.computation > 0 for task in TT):
            for T in TT:
                libs.Debug_Output.message(f"Schedule is infeasible if any TT task has ci > 0 at this point", t, T)
            sys.exit(1)

        with open("output.csv", "w") as file:
            file.write(csv_header + '\n')
            for csv_line in csv_content:
                file.writelines(csv_line+'\n')

        df = pd.read_csv('output.csv')
        df.plot()
        plt.show()

        # print(f"{schedule}")
        wcrt = [task.wcrt for task in TT]
        # print(wcrt)

        return schedule, wcrt