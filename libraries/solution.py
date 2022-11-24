import copy

import libraries as libs

class SolutionModel:
    def __init__(self, schedule, cost, PT_created, schedulable = False):
        self.schedule = schedule
        self.cost = cost
        self.PT_created = PT_created
        self.schedulable = schedulable

class Solution:
    @staticmethod
    def schedule(TT, ET, ):
        # Add time triggered polling tasks, if any
        TT_PT, ET_WCRT, PT_created = libs.PollingServer.add_PT(copy.deepcopy(TT), copy.deepcopy(ET))
        print(f'\n TT_PT: {TT_PT}', '\n event_triggered_tasks: {ET}')

        # Get schedule table and worst-case response times
        schedule, TT_WCRT, schedulable = libs.AlgoOne.scheduling_TT(copy.deepcopy(TT_PT))

        # Initial solution [schedule table, cost ]
        cost = libs.Functions.cost_function(TT_WCRT, ET_WCRT)
        solution = SolutionModel(schedule, cost, PT_created, schedulable)

        return solution

    @staticmethod
    # Finds the best solution which is the one with min cost
    def select_best_solution(solutions):
        best_solution = SolutionModel([], 10000000, 0)
        for solution in solutions:
            print('Proposed Solution:', solution.cost, solution.PT_created)
            if solution.cost < best_solution.cost:
                best_solution = solution

        print('#'*50)
        libs.Debug_Output.show_solution('Final Solution for TTs and TPs with ', best_solution)
        print('#'*50)

        return best_solution

    @staticmethod
    def search_solution(csv):
        # CONSTANTS
        #ET = []
        #TT = []
        TT, ET = libs.CSVReader.get_tasks_from_csv(csv)

        sep_counter = libs.Functions.count_separations(ET)

        # Get an initial solution to start the simulated annealing later
        initial_solution = libs.Solution.schedule(TT, ET)

        libs.Debug_Output.show_solution('Initial solution for TTs and TPs with ', initial_solution)

        solutions = []

        while len(solutions) < 5:
            print('Accepted solutions found so far: ', len(solutions))
            # Trigger simulated annealing
            proposed_solution = libs.simulated_annealing(initial_solution, TT, ET)

            libs.Debug_Output.show_solution('SA proposed solution for TTs and TPs with ', proposed_solution)

            # Validate solution is schedulable
            if not proposed_solution.schedulable:
                continue

            # Validate proposed_solution cost
            if proposed_solution.cost == 0:
                continue

            # Validate proposed_solution has right amount of PTs
            if proposed_solution.PT_created < sep_counter:
                continue

            solutions.append(proposed_solution)

        # Chose solution based on the min cost
        final_solution = libs.Solution.select_best_solution(solutions)

        libs.Functions.print_schedule(final_solution.schedule)

        return final_solution, solutions