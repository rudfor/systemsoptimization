# This is a sample Python script.

class TaskModel:
    """
    Missing line 21 and 22
    Add getters and setters
    """
    def __init__(self, name, duration, period, type, priority, deadline, separation = 0):
        self.name = name
        self.duration = int(duration) # ci computation
        self.init_duration = int(duration) # Ci
        self.period = int(period)     # Ti
        self.type = type
        self.priority = int(priority) # P
        self.deadline = int(deadline) # d
        self.init_deadline = int(deadline) # D
        self.separation = int(separation)

        self.r = 0 # worst-case response time
        self.wcrt = 0

def get_idle():
    return TaskModel('iddle', -1, -1, 'Idle', -1, -1)