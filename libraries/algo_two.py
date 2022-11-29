import sys
import copy
import math
import libraries as libs


class AlgoTwo:
    """
    # algorithm 2
    """

    @staticmethod
    def scheduling_ET(Cp, Tp, Dp, ET):
        """
        Data: Polling task budget Cp, polling task period Tp, polling task deadline Dp,
        subset of ET tasks to check T^ET
        Result: {true, false}, responseTime

        Cp = Polling task budget
        Tp = Polling task period
        Dp = Polling task deadline
        ET = Subset of event tasks
        """

        """
        Hints: (from pdf)
        1. (Not implemented yet) 
        In your first versions of the solution, consider the number of polling servers as a parameter.
        Start with one polling server and then increase manually the number of polling servers, e.g., 2, 3.

        2. (Implemented a simple version in Functions)
        For a given polling server, the search space for the period can be between 2 and the
        hyperperiod of all TT tasks.

        3. You can reduce the search space by considering in your first versions of the solution that
        the server deadline is be equal to the server period.

        4. You need to search for the “best” server budget. However, in the first versions of your
        solution, you can use a Hill Climbing approach based on a “binary search”, i.e., searching
        from 1 until the current server period and use the value that optimizes the cost function
        as the server budget.

        5. Allow your search to visit solutions which are not “feasible”, that is, TT or ET tasks
        may not be schedulable. That is, do not reject such solutions as being invalid. Instead,
        “penalize” these solutions using a penalty value.

        6. If you use Simulated Annealing or similar local search algorithms, e.g., Tabu Search, you
        may need to combine the TT and ET worst-case response times into a “weighted sum” [6].
        In this case, you may need to normalize the terms of the weighted sum, and also consider
        these normalization in relation to the penalty values, see earlier point
        """
        # ∆ ← Tp + Dp − 2 · Cp;
        delta = Tp + Dp - (2 * Cp)
        # print('init delta:', delta)
        # print('Tp', Tp, 'Cp', Cp, 'Dp', Dp)

        # α ← Cp/ Tp
        alpha = Cp / Tp
        # print('init alpha:', alpha)

        # /* The hyperperiod is the least common multiple of all task periods in T^ET */
        # T ← lcm{Ti | ∀τi ∈ T ET };
        T = libs.Functions.lcm(copy.deepcopy(ET))  # time limit
        # print(f"ET lcm: ", T)

        responseTime = 0
        response_times = dict()
        for task in ET:
            time = 0

            # Initialize the response time of τi to a value exceeding the deadline
            # responseTime ← Di + 1
            responseTime = task.deadline + 1

            # Remember, we are dealing with constrained deadline tasks, hence, in the
            # worst case arrival pattern, the intersection must lie within the
            # hyperperiod if the task set is schedulable.

            while time < T:
                # The supply at time t (c.f. [1])
                # supply ← α · (t − ∆);
                supply = max(0, alpha * (time - delta))

                # Compute the maximum demand at time t according to Eq. 2
                # demand ← 0 ;
                demand = 0

                # for τj ∈ T^ET with pj ≥ pi do
                for task_j in ET:
                    if (task_j.priority >= task.priority):
                        # demand ← demand + roundup(t/Tj) · Cj;
                        demand = demand + math.ceil(time / task_j.period) * task_j.computation

                # According to Lemma 1 of [1], we are searching for the earliest time,
                # when the supply exceeds the demand
                # if supply ≥ demand then
                if supply >= demand and supply > 0 and demand > 0:
                    # print('task name', task.name, 'supply', supply, 'demand', demand)
                    # responseTime ← t;
                    responseTime = time
                    response_times[task] = responseTime
                    break

                # Tick the clock
                time += 1

            # If for any task the intersection of the demand and supply are larger
            # than the task deadline, the task set T^ET is not schedulable using the
            # given polling task parameters.
            # if responseTime > Di then
            if responseTime > task.deadline:
                # print('responseTime:', responseTime, 'Di:', task.deadline)
                return False, responseTime

        return True, sum(rt for t, rt in response_times.items())
