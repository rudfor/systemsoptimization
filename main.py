import sys
import libraries as libs

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def schedule(TT, ET, time_limit=10000):
    """
    TT = Time Triggered
    ET = Event Triggerd
         Sporadic
    EDF = Earliest Deadline First
    RM = Rate Monotonic
    WCET = Worst Case Execution Time
    pi => task priority
    Di => relative deadline
    Ci => Compution time
    TT => Ti Period
    EF => Ti Sporadic
    :param T:
    :return:
    """

    # Get least common multiple of task priorities
    time_limit = libs.Functions.lcm(TT) or time_limit
    print(f"lcm: ", time_limit)

    # Start time
    t = 0

    # Init schedule table
    schedule = [0] * time_limit

    # We go through each time slot in until we reach the time limit
    while t < time_limit:
        # print(f"EDF: {libs.Functions.edf(t, TT.tasks).name}")
        for T in TT:
            # print(f"{T.name}")

            # Check time has not passed task deadline
            if T.duration > 0 and T.deadline <= t:
                libs.Debug_Output.message(f"Deadline Missed", t, T)
                sys.exit(1)

            # Check time is behind task deadline
            if T.duration == 0 and T.deadline >= t:
                # Check wcrt is the maximum response time over all T jobs
                # libs.Debug_Output.message(f"Check if the current WCRT {t - T.r} is larger than the current maximum {T.wcrt}", t, T)
                if (t - T.r) >= T.wcrt:
                    # Update max
                    T.wcrt = t - T.r

            # When task is completed we should reset its duration and move deadline to the present
            if t % T.period == 0:
                T.r = t
                T.duration = T.init_duration
                T.deadline = T.init_deadline + t
                print(T.name, T.duration, T.init_deadline, T.deadline, t)

        # Check if there is any tasks with computation left
        if all(task.duration == 0 for task in TT):
            # If no task has computation left, schedule idle slot
            schedule[t] = libs.get_idle()
        else:
            # Get task with earliest deadline
            ti = libs.Functions.edf(TT, t)

            # Add task to the current second in the schedule
            # print(f"add to schedule {ti.name} at {t}")
            schedule[t] = ti

            # Since we execute the task in the current second then we
            # reduce by one time second the remaining duration of the task
            ti.duration -= 1
            TT = libs.Functions.update_duration(TT, ti)

        # Tick the clock
        t += 1

    # If at least one task has its duration more than 0 that indicates
    # that at least one task is not completed and therefore the schedule
    # is infeasible for the given combination of tasks in the given time limit.
    if any(task.duration >= 0 for task in TT):
        libs.Debug_Output.message(f"Schedule is infeasible if any TT task has ci > 0 at this point", t, T)
        sys.exit(1)

    # print(f"{schedule}")
    wcrt = [task.wcrt for task in TT]
    # print(wcrt)

    return schedule, wcrt

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Ask user for file input
    csv = input("CSV path file: ") or 'resources/tasks.txt'

    # Extract time triggered tasks from csv
    time_triggered_task = libs.CSVReader.get_tasks(csv, 'TT', True)
    if (len(time_triggered_task) <= 0):
        print(f"<{csv}> is empty or was not properly formed")
        exit(1)
    print(f"{time_triggered_task}")

    # Get schadule table and worst-case response times
    schedule, WCRT = schedule(time_triggered_task, [])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
