import numpy as np

class Functions():
    @staticmethod
    def edf(tasks, current_time):
        task = None
        for ti in tasks:
            if ti.duration > 0 and (task is None or ti.deadline < task.deadline):
                # print(ti.duration)
                task = ti
        return task

    @staticmethod
    def update_duration(TT, task):
        for ti in TT:
            if ti.name == task.name:
                ti.duration = task.duration
        return TT

    @staticmethod
    def lcm(TT):
        periods = [task.period for task in TT]
        return np.lcm.reduce(periods)

    @staticmethod
    def printSchedule(schedule):
        for time, T in enumerate(schedule):
            print('Scedule time:', time, 'On going task:', T.name, T.duration, T.init_deadline, T.deadline)

class Debug_Output:
    @staticmethod
    def message(message, time, Task):
        print('_'*100)
        print(f"{message}: at {time} for {Task.name}")
        print(f"Current time: {time}")
        print(f"Duration: {Task.duration}")
        print(f"Deadline: {Task.deadline}")
        print(f"Period: {Task.period}")
        print(f"Current time after execution: {time + Task.duration}")