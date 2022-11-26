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
    def scheduling_TT(TT, time_limit=10000, visuals = False):
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
        # FAIL_WCRT and FAIL_SCHEDULE will be the attributes we will set
        # as a 'solution' when TT and PT are not schedulable.
        # We do this in order to penalize the 'wrong solutions' so then
        # the simulated_annealing will discard them and try another solution
        FAIL_WCRT = 99999999999
        FAIL_SCHEDULE = []

        # Get least common multiple of task priorities
        time_limit = libs.Functions.lcm(copy.deepcopy(TT)) or time_limit
        print(f"\n TT lcm: ", time_limit)

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
            for T in TT:
                # Check time has not passed task deadline
                if T.computation > 0 and T.deadline <= t:
                    libs.Debug_Output.message(f"\n Deadline Missed", t, T)
                    return FAIL_SCHEDULE, FAIL_WCRT, False

                # When task is completed we should reset its duration and move deadline to the present
                if t % T.period == 0:
                    T.r = t
                    T.computation = T.init_computation
                    T.deadline = T.init_deadline + t
                    # print('\n reset on period', T.name, T.computation, T.init_deadline, T.deadline, t)

                if csv_line:
                    csv_line = f'{csv_line}, {T.computation}'
                else:
                    csv_line = f'{T.computation}'

            csv_content.append(csv_line)

            # Check if there is any tasks with computation left
            if all(task.computation == 0 for task in TT):
                # If no task has computation left, schedule idle slot
                schedule[t] = libs.get_idle()
            else:
                # Get task with earliest deadline
                ti = libs.Functions.edf(TT, t)

                # Add task to the current second in the schedule
                schedule[t] = copy.deepcopy(ti)

                # Since we execute the task in the current second then we
                # reduce by one time second the remaining duration of the task
                ti.computation -= 1

                # this is the 3rd time i move the code down here
                # Check time is behind task deadline
                if ti.computation == 0 and ti.deadline >= t:
                    # Check wcrt is the maximum response time over all T jobs
                    if (t - ti.r) >= ti.wcrt:
                        # Update max
                        ti.wcrt = t - ti.r

            # Tick the clock
            t += 1

            if watchDog < 0:
                print('\n Force break triggered of scheduling of TT tasks...')
                break
            watchDog -= 1

        # If at least one task has its duration more than 0 that indicates
        # that at least one task is not completed and therefore the schedule
        # is infeasible for the given combination of tasks in the given time limit.
        if any(task.computation > 0 for task in TT):
            for T in TT:
                libs.Debug_Output.message(f"\n Schedule is infeasible if any TT task has ci > 0 at this point", t, T)
            return FAIL_SCHEDULE, FAIL_WCRT, False

        if visuals:
            with open("output/output.csv", "w") as file:
                file.write(csv_header + '\n')
                for csv_line in csv_content:
                    file.writelines(csv_line + '\n')

            df = pd.read_csv('output/output.csv')
            df.plot()
            plt.show()

        wcrt = sum(task.wcrt for task in TT)

        return schedule, wcrt, True