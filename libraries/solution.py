import copy
import sys

import libraries as libs

class SolutionModel:
    def __init__(self, schedule, cost, schedulable = False, config = None):
        self.schedule = schedule
        self.cost = cost
        self.schedulable = schedulable
        self.config = config

class ConfigModel:
    def __init__(self, TT, ET, PT):
        self.TT = TT
        self.ET = ET
        self.PT = PT

class Solution:
    @staticmethod
    def schedule(config):
        TT = config.TT
        PT = config.PT

        PT_schedulable, ET_WCRT = libs.PollingServer.check_polling_tasks_schedulability(copy.deepcopy(PT))

        # Add time triggered polling tasks, if any
        # TT_PT, ET_WCRT, PT_created = libs.PollingServer.add_PT(copy.deepcopy(TT), copy.deepcopy(ET))
        # print(f'\n TT_PT: {TT_PT}', '\n event_triggered_tasks: {ET}')

        # Get schedule table and worst-case response times
        TT_and_PT = TT + PT
        schedule, TT_WCRT, TT_schedulable = libs.AlgoOne.scheduling_TT(copy.deepcopy(TT_and_PT))
        # print(TT_WCRT)
        TT_WCRT = TT_WCRT if TT_schedulable else TT_WCRT + [1000]

        # Get solution cost
        cost = libs.Functions.cost_function(TT_WCRT, ET_WCRT)

        return SolutionModel(schedule, cost, TT_schedulable and PT_schedulable, config)

    @staticmethod
    # Finds the best solution which is the one with min cost
    def select_best_solution(solutions):
        best_solution = SolutionModel([], 50000)
        for solution in solutions:
            print('Proposed Solution:', solution.cost)
            if solution.cost < best_solution.cost:
                best_solution = solution

        print('#'*50)
        libs.Debug_Output.show_solution('Final Solution for TTs and TPs with ', best_solution)
        print('#'*50)

        return best_solution

    @staticmethod
    def search_solution(csv):
        TT, ET = libs.CSVReader.get_tasks_from_csv(csv)

        # GET INITIAL SOLUTION
        # It will be used to start the optimization of simulated annealing later
        initial_solution = Solution.get_init_solution(TT, ET)
        libs.Debug_Output.show_solution('Initial solution for TTs and TPs with ', initial_solution)

        solutions = []

        # TODO: All this can also be removed and just increase the SA initial temperature
        #  to force it run longer. Just keep one single invoke of SA in the end. Unless we
        #  never make it good enough on one single go and then we can keep the more attempts.
        while len(solutions) < 5:
            print('Accepted solutions found so far: ', len(solutions))

            # TRIGGER SA
            proposed_solution = libs.simulated_annealing(initial_solution)
            libs.Debug_Output.show_solution('SA proposed solution for TTs and TPs with ', proposed_solution)

            # Validate solution is schedulable
            if not proposed_solution.schedulable:
                continue

            # Validate proposed_solution cost
            if proposed_solution.cost == 0:
                continue

            solutions.append(proposed_solution)

        # Chose solution based on the min cost
        final_solution = libs.Solution.select_best_solution(solutions)

        libs.Functions.print_schedule(final_solution.schedule)

        return final_solution, solutions


    @staticmethod
    def get_init_solution(TT, ET):
        # Distribute events
        events_grouped = libs.Functions.get_event_sublists(ET)

        lcmTT = libs.Functions.lcm(TT)
        lcmET = libs.Functions.lcm(ET)

        # SET AN INITIAL EVENT DISTRIBUTION AND PT HYPERPARAMETERS
        PTs = []
        for separation, events in events_grouped.items():
            # Init polling task
            computation = sum(t.computation for t in events)
            pt = libs.get_polling(separation, computation, 2000, events)

            # Init period
            pt.period = libs.Functions.get_polling_task_period(lcmTT, lcmET)

            # Init budget
            pt.budget = libs.Functions.get_polling_task_budget(ET)

            # Init assigned events
            pt.assignedEvents = events_grouped[pt.separation]

            pt.deadline = libs.Functions.get_pooling_task_deadline(events_grouped[pt.separation])

            PTs.append(pt)

        # SET INITIAL CONFIG
        config = ConfigModel(TT, ET, PTs)

        # CREATE AND RETURN INITIAL SOLUTION
        return libs.Solution.schedule(config)
