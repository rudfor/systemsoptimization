import sys
import copy
import math
import libraries as libs

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# algorithm 1
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


# algorithm 2
def schedulingET(Cp, Tp, Dp, ET):
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
    delta = Tp + Dp - (2*Cp)
    # print('init delta:', delta)

    # α ← Cp/ Tp
    alpha = Cp/Tp
    # print('init alpha:', alpha)

    # /* The hyperperiod is the least common multiple of all task periods in T^ET */
    # T ← lcm{Ti | ∀τi ∈ T ET };
    T = libs.Functions.lcm(copy.deepcopy(ET))  # time limit
    # print(f"ET lcm: ", T)

    responseTime = 0
    for task in ET:
        time = 0

        # Initialize the response time of τi to a value exceeding the deadline
        # responseT ime ← Di + 1
        responseTime = task.deadline + 1

        # Remember, we are dealing with constrained deadline tasks, hence, in the
        # worst case arrival pattern, the intersection must lie within the
        # hyperperiod if the task set is schedulable.

        while time < T:
            # The supply at time t (c.f. [1])
            # supply ← α · (t − ∆);
            supply = alpha * (time - delta)

            # Compute the maximum demand at time t according to Eq. 2
            # demand ← 0 ;
            demand = 0

            # for τj ∈ T^ET with pj ≥ pi do
            for task_j in ET:
                if (task_j.priority >= task.priority):
                    # demand ← demand + roundup(t/Tj) · Cj;
                    demand = demand + math.ceil(time/task_j.period) * task_j.computation

            # According to Lemma 1 of [1], we are searching for the earliest time,
            # when the supply exceeds the demand
            # if supply ≥ demand then
            if supply >= demand:
                # print('task name', task.name, 'supply', supply, 'demand', demand)
                # responseTime ← t;
                responseTime = time
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

    return True, responseTime


# usage of algorithm 2
def addPollingTasks(TT, ET, PTs = 1):
    # When no ET given, return TT as given
    if len(ET) < 1:
        return TT

    # Identify all given separations
    separations = []
    for task in ET:
        if task.separation not in separations:
            separations.append(task.separation)
    # Sort asc
    separations.sort()

    # For a given polling server, the search space for the period can be
    # between 2 and the hyperperiod of all TT tasks (2nd hint in pdf)
    lcm = libs.Functions.lcm(copy.deepcopy(TT))
    period = libs.Functions.getPollingTaskPeriod(lcm)
    print('Polling period:', period)

    # Add polling tasks for as many separations is requested
    while PTs > 0 and len(separations) > 0:
        # Find a separation which tasks can be schedulable
        foundSchedulableSeparation = False
        while not foundSchedulableSeparation and len(separations) > 0:
            bestBudget = 0
            worstResponseTime = 900000000

            # Get first available separation
            # 1
            separation = separations.pop(0)

            # Hill Climbing until found the best budget for polling task, if any
            attemptsDuringPlateau = 3
            for budget in range(1, period):
                # Get sublist of ET tasks with the same separation
                sublistET = []
                for task in ET:
                    # Fetch the ET tasks with current separation and with non-separation (zero)
                    if task.separation in [0, separation]:
                        sublistET.append(task)

                # Init the polling task attributes
                pollingTask = [budget, period, period]  # [budget, period, deadline = period]

                # Check if sublistET is schedulable
                schedulable, responseTime = schedulingET(pollingTask[0], pollingTask[1], pollingTask[2], sublistET)

                # If separation is schedulable for budget then we store best responseTime and its budget.
                # Here we use response time as cost of our binary search in order to determine the best budget.
                if (schedulable == True and responseTime <= worstResponseTime):
                    worstResponseTime = responseTime
                    foundSchedulableSeparation = True

                    # Decrease attempts during plateau
                    if worstResponseTime == responseTime:
                        attemptsDuringPlateau -= 1

                    # Terminate search once consumed all plateau attempts
                    if attemptsDuringPlateau < 1:
                        break
                    bestBudget = budget

        if foundSchedulableSeparation:
            # Create polling task
            task = libs.get_polling(separation, bestBudget, period)

            # Add polling task to Time Triggered tasks
            print('Add pooling schedulable task with separation:', separation, 'and budget:', bestBudget, 'and period:', period)
            TT.append(task)

            PTs -= 1

    return TT


# usage of addPollingTasks and usage 1
def schedule(csv):
    # Extract time triggered tasks from csv
    time_triggered_tasks = libs.CSVReader.get_tasks(csv, 'TT', False)
    if (len(time_triggered_tasks) <= 0):
        print(f"<{csv}> is empty or was not properly formed")
        exit(1)

    # Extract event triggered tasks from csv
    event_triggered_tasks = libs.CSVReader.get_tasks(csv, 'ET', False)
    if (len(event_triggered_tasks) <= 0):
        print(f"<{csv}> has no event triggered tasks")

    # Add time triggered polling tasks, if any
    time_triggered_tasks = addPollingTasks(time_triggered_tasks, event_triggered_tasks, 1)

    # Get schedule table and worst-case response times
    schedule, WCRT = schedulingTT(time_triggered_tasks)

    libs.Functions.printSchedule(schedule)

    return schedule, WCRT


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Ask user for file input
    csv = input("CSV path file: ") or 'resources/tasks.txt'

    # Init scheduling
    schedule(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
