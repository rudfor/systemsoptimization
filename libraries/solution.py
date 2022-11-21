import libraries as libs

class SolutionModel:
    def __init__(self, schedule, cost, PT_created):
        self.schedule = schedule
        self.cost = cost
        self.PT_created = PT_created

class Solution:
    @staticmethod
    def schedule(TT, ET):
        # Add time triggered polling tasks, if any
        TT_PT, ET_WCRT, PT_created = libs.PollingServer.add_PT(TT, ET)
        print(f'\n TT_PT: {TT_PT}', '\n event_triggered_tasks: {ET}')

        # Get schedule table and worst-case response times
        schedule, TT_WCRT = libs.AlgoOne.scheduling_TT(TT_PT)

        # Initial solution [schedule table, cost ]
        cost = libs.Functions.cost_function(TT_WCRT, ET_WCRT)
        solution = SolutionModel(schedule, cost, PT_created)

        return solution

    @staticmethod
    # Finds the best solution which is the one with min cost
    def select_best_solution(solutions):
        best_solution = SolutionModel([], 10000000, 0)
        for solution in solutions:
            print('Solution:', solution.cost, solution.PT_created)
            if solution.cost < best_solution.cost:
                best_solution = solution

        return best_solution