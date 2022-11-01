import numpy as np
import random

class Functions():
    @staticmethod
    def edf(tasks, current_time):
        task = None
        for ti in tasks:
            if ti.computation > 0 and (task is None or ti.deadline < task.deadline):
                # print(ti.computation)
                task = ti
        return task

    @staticmethod
    def update_duration(TT, task):
        for ti in TT:
            if ti.name == task.name:
                ti.computation = task.computation
        return TT

    @staticmethod
    def lcm(tasks):
        periods = [task.period for task in tasks]
        return np.lcm.reduce(periods)

    @staticmethod
    def printSchedule(schedule):
        for time, T in enumerate(schedule):
            print('Scedule time:', time, 'On going task:', T.name, T.computation, T.init_deadline, T.deadline, T.separation)

    @staticmethod
    def getPollingTaskPeriod(lcm):
        # For a given polling server, the search space for the period
        # can be between 2 and the hyperperiod (lcm) of all TT tasks.
        period = 0.00003 # init with any bad multiplier

        # take any common multiplier as period to make my life easier otherwise we have
        # to iterate from 2 till lcm for every budget=[1, period], which is insane
        # TODO: find the best period somehow
        while not period % lcm == 0:
            period = random.randint(2, lcm)
        return period

class Debug_Output:
    @staticmethod
    def message(message, time, Task):
        print('_'*100)
        print(f"{message}: at {time} for {Task.name}")
        print(f"Current time: {time}")
        print(f"Duration: {Task.computation}")
        print(f"Deadline: {Task.deadline}")
        print(f"Period: {Task.period}")
        print(f"Current time after execution: {time + Task.computation}")