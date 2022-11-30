import sys

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

    # @staticmethod
    # def update_duration(TT, task):
    #     for ti in TT:
    #         if ti.name == task.name:
    #             ti.computation = task.computation
    #     return TT

    @staticmethod
    def lcm(tasks):
        periods = [task.period for task in tasks]
        return np.lcm.reduce(periods)

    @staticmethod
    def computation(tasks, verbose=False):
        compute = [task.computation for task in tasks]
        if verbose:
            print(f'{compute}')
        return sum(compute)

    @staticmethod
    def deadline(tasks, verbose=False):
        compute = [task.deadline for task in tasks]
        if verbose:
            print(f'{compute}')
        return min(compute)


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

    # @staticmethod
    # def get_polling_task_budget(period):
    #     return int(random.randint(1, period))

    @staticmethod
    # lcm of time triggered task
    def get_polling_task_period(lcm, previous_period = None):
        # get lcm factors
        lcmFactors = Functions.get_factors(lcm)

        lcmFactors = [x for x in lcmFactors if x >= 500 and x <= 6000]
        # print('lcmFactors', lcmFactors)

        if previous_period is not None:
            previous_index = lcmFactors.index(previous_period)
            next_index = previous_index + random.randint(-1, 1)
            factor = lcmFactors[next_index] if next_index <= len(lcmFactors)-1 else random.choice(lcmFactors)
        else:
            # pick any factor
            factor = random.choice(lcmFactors)

        # return a PT period that is in harmony with lcm
        return int(factor)

    @staticmethod
    def get_polling_task_budget(ET, previous_budget = None):
        next_budget = 0
        if previous_budget is None:
            next_budget = 0
            for event in ET:
                next_budget += event.computation
        else:
            next_budget = previous_budget + 100

        return int(next_budget)

    @staticmethod
    def cost_function(TT_WCRT, ET_WCRT):
        # print('TT_WCRT + ET_WCRT', TT_WCRT, ET_WCRT)
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
    def get_event_sublists(ET, seed=None, verbose=False):
        # Seed initial value
        if seed is not None:
            random.seed(seed)
        else:
            random.seed()

        # initialize event sublists
        sublistETs = dict()

        # Get sublist of ET tasks with the same separation also for zeros
        for event in ET:
            if event.separation not in sublistETs.keys():
                sublistETs[event.separation] = []
            sublistETs[event.separation].append(event)

        # Check if we have events with zero separation and
        # split them among the rest of the separations randomly
        #
        # Code block bellow will do the following:
        # From:  {0: [ET1,ET2], 1: [ET3], 2: [ET4]}
        # To:    {1: [ET3,ET1], 2: [ET4,ET2]}
        if 0 in sublistETs.keys() and len(sublistETs) > 1:
            # get the events of the key for zero separation
            # and remove the key from sublistETs
            zeros = sublistETs.pop(0, None)

            # Split events with zero separation among the rest of separations
            # Adds one zero_event to each of the rest of the separations and
            # until all zero_events are all distributed completely
            if verbose: print('\n')
            if verbose: print('All sublistETs: ', sublistETs)
            separations = list(sublistETs.keys())
            while len(zeros) > 0:
                chose_separations = random.choice(separations)
                if chose_separations == 0:
                    continue
                # get an event from the zeros
                zeroEvent = zeros.pop()

                # and add it to the current separation
                sublistETs[chose_separations].append(zeroEvent)

            if verbose: print('Distributed zeros sublistETs:', sublistETs)
        return sublistETs

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
              f"schedulable: {solution.schedulable}")