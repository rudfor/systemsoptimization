import sys
import re
import os
import csv
# This is a sample Python script.

class Functions():
    @staticmethod
    def edf(tasks):
        counter = 0
        least_name = tasks[0].name
        least_deadline = tasks[0].deadline
        for task in tasks[1:]:
            if task.deadline < least_deadline:
                least_name = task.name
                least_deadline = task.deadline
        return least_name


class Tasks:
    def __init__(self, csv_file, task_type=None, verbose=False):
        self.csv_file = csv_file
        self.task_type = task_type
        self.verbose = verbose
        self.tasks = ReadTasks.get_tasks(self.csv_file, self.task_type, self.verbose)

    # def __call__(self):
    #     return [self.tasks]
    """
    Read File into list of Tasks
    """
    def get_tasks(self):
        return self.tasks

    def edf(self):
        counter = 0
        least_name = self.tasks[0].name
        least_deadline = self.tasks[0].deadline
        for task in self.tasks[1:]:
            if task.deadline < least_deadline:
                least_name = task.name
                least_deadline = task.deadline
        return least_name



class ReadTasks():
    """
    Read File into list of Tasks
    """
    @staticmethod
    def get_tasks(csf_file, task_type=None, verbose=False):
        list = []
        with open(csf_file) as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                if not len(row):
                    if verbose: print(f"EMPTY LINE")
                elif len(row) == 7:
                    if verbose: print(f"VALID")
                    name, duration, period, t_type, priority, deadline, separation = row
                    if task_type is None:
                        list.append(Task(name, duration, period, t_type, priority, deadline, separation))
                    elif task_type == t_type:
                        list.append(Task(name, duration, period, t_type, priority, deadline, separation))
                    else:
                        if verbose: print(f"rows {row}")
                else:
                    if verbose: print(f"INVALID {len(row)}")
        if verbose: print(list)
        return list


class Task:
    """
    Missing line 21 and 22
    Add getters and setters
    """
    def __init__(self, name, duration, period, type, priority, deadline, separation):
        self.name = name
        self.duration = int(duration) # ci
        self.init_duration = int(duration) # Ci
        self.period = int(period)     # Ti
        self.type = type
        self.priority = int(priority) # P
        self.deadline = int(deadline) # d
        self.init_deadline = int(deadline) # D
        self.separation = int(separation)
        self.r = 0
        self.wcrt = 0


class Debug_Output:
    @staticmethod
    def message(message, time, Task, verbosity=False):
        print(f"{message}: at {time} for {Task.name}")
        print(f"Deadline: {Task.deadline}")
        print(f"Duration: {Task.duration}")
        print(f"leftover: {time + Task.duration}")



class Old_Examples:
    @staticmethod
    def print_hi(name):
        # Use a breakpoint in the code line below to debug your script.
        print(f"Hi, {name}")  # Press Ctrl+F8 to toggle the breakpoint.

    @staticmethod
    def get_tasks():
        tt = []
        tt.append(Task(tTT0, 1604, 10000, 'TT', 7, 1000, 0))
        tt.append(Task(tTT1, 46, 5000, 'TT', 7, 5000, 0))
        tt.append(Task(tTT2, 257, 10000, 'TT', 7, 10000, 0))
        tt.append(Task(tTT3, 51, 10000, 'TT', 7, 10000, 0))
        tt.append(Task(tET3, 958, 10000, 'ET', 0, 6107, 0))
        tt.append(Task(tET0, 349, 5000, 'ET', 4, 3799, 0))
        tt.append(Task(tET1, 59, 5000, 'ET', 6, 3221, 0))
        tt.append(Task(tET2, 114, 5000, 'ET', 6, 2575, 0))
        return tt

    @staticmethod
    def get_tt():
        TT = []
        TT.append(Task('tTT0', 1604, 10000, 'TT', 7, 1000, 0))
        TT.append(Task('tTT1', 46, 5000, 'TT', 7, 5000, 0))
        TT.append(Task('tTT2', 257, 10000, 'TT', 7, 10000, 0))
        TT.append(Task('tTT3', 51, 10000, 'TT', 7, 10000, 0))
        return TT

    @staticmethod
    def get_et():
        ET = []
        ET.append(Task(tET3, 958, 10000, 'ET', 0, 6107))
        ET.append(Task(tET0, 349, 5000, 'ET', 4, 3799))
        ET.append(Task(tET1, 59, 5000, 'ET', 6, 3221))
        ET.append(Task(tET2, 114, 5000, 'ET', 6, 2575))
        return ET


if __name__ == '__main__':

    # file name with extension
    file_name = os.path.basename('/root/file.ext')

    # file name without extension
    print(os.path.splitext(file_name)[0])