# This is a sample Python script.
import libraries as libs
from operator import attrgetter

class TaskModel:
    """
    We denote the set of TT and ET tasks with TT^T and T^ET , respectively.
    A TT or ET task τi is defined by the tuple (pi , Ci , Ti , Di) with
    Ci denoting the computation time (computation=duration for us),
    pi is the task priority, and
    Di the relative deadline of the task.

    For TT tasks, Ti represents the period,
    while for ET tasks, where we assume a sporadic model,
    it describes the minimal inter-arrival distance (MIT)
    """
    def __init__(self, name, computation, period, type, priority, deadline, budget=0, separation=0, assigned_events=None):
        self.name = name
        self.computation = int(computation) # ci computation
        self.init_computation = int(computation) # Ci initial computation
        self.period = int(period)     # Ti
        self.type = type
        self.priority = int(priority) # P
        self.deadline = int(deadline) # d
        self.init_deadline = int(deadline) # D
        self.separation = int(separation)
        self.budget = int(budget)
        self.assignedEvents = assigned_events
        self.budget = period

        self.r = 0 # worst-case response time
        self.wcrt = 0

    def compute(self, verbosity = 0):
        if verbosity > 3: print(f'PREQUEL: -{self.assignedEvents}\n')
        if self.assignedEvents is not None:
            if libs.Functions.computation(self.assignedEvents) > 0:
                if verbosity > 3: print(f'BEFORE: {self.computation}-{self.assignedEvents}\n')
                edf_task = min([task for task in self.assignedEvents if task.computation!=0], key=attrgetter('deadline'))
                edf_task.computation -= 1
                if verbosity > 3: print(f'EDF_TASK: {edf_task}\n')
                if verbosity > 3: print(f'calculate Computation: {libs.Functions.computation(self.assignedEvents)}\n')
                self.compusation = libs.Functions.computation(self.assignedEvents)
                deadline_list = [task.deadline for task in self.assignedEvents if task.computation != 0]
                if not deadline_list:
                    pass
                else:
                    deadline = min(deadline_list)
                    self.deadline = deadline
                if verbosity > 3: print(f'AFTER: {self.computation}-{self.assignedEvents}\n')
        else:
            self.computation -= 1

    def reset_compute(self, verbosity = 0):
        if verbosity > 3: print(f'PREQUEL: -{self.assignedEvents}\n')
        if self.assignedEvents is not None:
            if libs.Functions.computation(self.assignedEvents) > 0:
                pass
        else:
            self.computation = self.init_computation

    def __repr__(self):
        if self.assignedEvents is None:
            return_string = f'Task: '
            return_string += f'name({self.name}) '
            return_string += f'computation({self.computation}) '
            return_string += f'period({self.period}) '
            return_string += f"type({self.type}) "
            return_string += f"deadline({self.deadline}) "
            return_string += f"separation({self.separation})"
        else:
            return_string = f'Task: '
            return_string += f'name({self.name}) '
            return_string += f'computation({self.computation}) '
            return_string += f'period({self.period}) '
            return_string += f"type({self.type}) "
            return_string += f"deadline({self.deadline}) "
            return_string += f"separation({self.separation})"
            for et in self.assignedEvents:
                return_string += f"\n\t{et.__repr__()}"

        return return_string

    def __hash__(self):
        return hash((self.__repr__()))

def get_idle():
    return TaskModel('idle', -1, -1, 'Idle', -1, -1)

def get_polling(separation, budget, period, assignedEvents):
    # deadline = period based on 3rd pdf hint
    # priority can be 7 since polling tasks are time triggered tasks
    return TaskModel(f'tPT{str(separation)}', budget, period, 'PT', 7, period, separation, assignedEvents)
