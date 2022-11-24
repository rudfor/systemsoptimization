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
    def get_factors(number: int):
        factors = []
        factor = 1
        while factor <= number:
            if number % factor == 0:
                factors.append(factor)
            factor += 1
        return factors

    @staticmethod
    def print_schedule(schedule):
        for time, T in enumerate(schedule):
            print('Schedule time:', time, 'On going task:', T.name, T.computation, T.init_deadline, T.deadline, T.separation)

    @staticmethod
    def get_polling_task_budget(period):
        return int(random.randint(1, period))


    @staticmethod
    def get_polling_task_period(lcm):
        # get lcm factors
        lcmFactors = Functions.get_factors(lcm)

        # pick any factor
        factor = random.choice(lcmFactors)

        # return a PT period that is in harmony with lcm
        return int(factor) if factor >= 2000 else 2000

    @staticmethod
    def cost_function(TT_WCRT, ET_WCRT):
        return TT_WCRT + ET_WCRT

    @staticmethod
    def get_separations(ET):
        # Identify all given separations
        separations = []
        for task in ET:
            if task.separation not in separations:
                separations.append(task.separation)
        # Sort asc
        separations.sort()

        # Treat zero separation as individual if its the only one in the ET
        # Or if we have more separations then remove zero separation from the
        # independent separations
        # ex: [0] then we keep it [0]
        # ex: [0,1,2,3] then we remove zero [1,2,3]
        if len(separations) > 1:
            separations.remove(0)

        return separations

    @staticmethod
    def count_separations(ET):
        # Identify all given separations
        separations = Functions.get_separations(ET)

        return len(separations)

    @staticmethod
    def dict_hash(the_dict, *ignore):
        if ignore:  # Sometimes you don't care about some items
            interesting = the_dict.copy()
            for item in ignore:
                if item in interesting:
                    interesting.pop(item)
            the_dict = interesting
        result = hashlib.sha1(
            '%s' % sorted(the_dict.items())
        ).hexdigest()
        return result


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

    @staticmethod
    def show_solution(message, solution):
        print(f"\n {message}"
              f"cost: {solution.cost} "
              f"created_PT: {solution.PT_created} and "
              f"schedulable: {solution.schedulable}")