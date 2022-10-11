import csv
from .task import TaskModel

"""
Read File into list of Tasks
"""
class CSVReader():
    def __init__(self, csv_file, verbose=False):
        self.csv_file = csv_file
        self.verbose = verbose

    @staticmethod
    def get_tasks(csf_file, task_type='TT', verbose=False):
        list = []
        with open(csf_file) as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                if not len(row):
                    if verbose: print(f"EMPTY LINE")
                elif len(row) == 7:
                    if verbose: print(f"VALID")
                    name, duration, period, t_type, priority, deadline, separation = row
                    if verbose: print(name, duration, period, t_type, priority, deadline, separation)
                    if task_type is None:
                        list.append(TaskModel(name, duration, period, t_type, priority, deadline, separation))
                    elif task_type == t_type:
                        list.append(TaskModel(name, duration, period, t_type, priority, deadline, separation))
                elif len(row) == 8:
                    if verbose: print(f"VALID")
                    tasks, name, duration, period, t_type, priority, deadline, separation = row
                    if verbose: print(name, duration, period, t_type, priority, deadline, separation)
                    if task_type is None:
                        list.append(TaskModel(name, duration, period, t_type, priority, deadline, separation))
                    elif task_type == t_type:
                        list.append(TaskModel(name, duration, period, t_type, priority, deadline, separation))
                    else:
                        if verbose: print(f"rows {row}")
                else:
                    if verbose: print(f"INVALID {len(row)}")
        if verbose: print(list)

        return list