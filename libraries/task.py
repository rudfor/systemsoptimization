# This is a sample Python script.

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
    def __init__(self, name, computation, period, type, priority, deadline, separation = 0, assigned_events = None):
        self.name = name
        self.computation = int(computation) # ci computation
        self.init_computation = int(computation) # Ci initial computation
        self.period = int(period)     # Ti
        self.type = type
        self.priority = int(priority) # P
        self.deadline = int(deadline) # d
        self.init_deadline = int(deadline) # D
        self.separation = int(separation)
        self.assignedEvents = assigned_events

        self.r = 0 # worst-case response time
        self.wcrt = 0

    def __repr__(self):
        return f"\n Task: " \
               f"name({self.name}) " \
               f"computation({self.computation}) " \
               f"period({self.period}) " \
               f"type({self.type}) " \
               f"deadline({self.deadline}) " \
               f"separation({self.separation})"

def get_idle():
    return TaskModel('idle', -1, -1, 'Idle', -1, -1)

def get_polling(separation, budget, period, assignedEvents):
    # deadline = period based on 3rd pdf hint
    # priority can be 7 since polling tasks are time triggered tasks
    return TaskModel(f'tPT{str(separation)}', budget, period, 'PT', 7, period, separation, assignedEvents)
