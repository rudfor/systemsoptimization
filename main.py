import sys
import re
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Task():
    """
    Missing line 21 and 22
    Add getters and setters
    """
    def __init__(self, name, duration, period, type, priority, deadline):
        self.name = name
        self.duration = duration # ci
        self.init_duration = duration # Ci
        self.period = period     # Ti
        self.type = type
        self.priority = priority # P
        self.deadline = deadline # d
        self.init_deadline = deadline # D
        self.r = 0
        self.wcrt = 0

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def get_tasks():
    TT = []
    TT.append(Task(tTT0, 1604,10000,TT,7,1000))
    TT.append(Task(tTT1, 46,5000,TT,7,5000))
    TT.append(Task(tTT2, 257,10000,TT,7,10000))
    TT.append(Task(tTT3, 51,10000,TT,7,10000))
    TT.append(Task(tET3, 958,10000,ET,0,6107))
    TT.append(Task(tET0, 349,5000,ET,4,3799))
    TT.append(Task(tET1, 59,5000,ET,6,3221))
    TT.append(Task(tET2, 114,5000,ET,6,2575))
    return TT

def get_tt():
    TT = []
    TT.append(Task('tTT0', 1604,10000,'TT',7,1000))
    TT.append(Task('tTT1', 46,5000,'TT',7,5000))
    TT.append(Task('tTT2', 257,10000,'TT',7,10000))
    TT.append(Task('tTT3', 51,10000,'TT',7,10000))
    return TT

def get_et():
    ET = []
    ET.append(Task(tET3, 958,10000,ET,0,6107))
    ET.append(Task(tET0, 349,5000,ET,4,3799))
    ET.append(Task(tET1, 59,5000,ET,6,3221))
    ET.append(Task(tET2, 114,5000,ET,6,2575))
    return ET


def schedule():
    """
    TT = Time Triggered
    ET = Event Triggerd
         Sporadic
    EDF = Earliest Deadline First
    RM = Rate Monotonic
    WCET = Worst Case Execution Time
    :param T:
    :return:
    """
    TT = get_tt()
    time_limit = 6000
    t = 0
    schedule = [0] * time_limit

    while t <= time_limit:
        wcrt = []
        #for t in range(time_limit,1): # while t < T do
        for T in TT:
            print(f"{T.name}")
            if T.duration > 0 and T.deadline >= t:
                print(f"Deadline Missed: {t}:{T.name}")
                print(f"Deadline: {T.deadline}")
                print(f"Duration: {T.duration}")
                print(f"leftover: {t+T.duration}")
                #sys.exit(1)
            if T.duration == 0 and T.deadline <= t:
                if (t - T.r) >= T.wcrt:
                    T.wcrt = (t - T.r)
                    wcrt.append(T.wcrt)
                print(f"Check WCRT: {t}:{T.name}")
                print(f"Deadline: {T.deadline}")
                print(f"Duration: {T.duration}")
                print(f"leftover: {t-T.duration}")
            if t % T.period == 0:
                T.r = t
                T.duration = T.init_duration
                T.deadline = T.init_deadline + t
        idle = True
        for T in TT:
            if T.duration > 0:
                print(f"Time at Idle: {t}")
                #schedule[t]='idle'
                idle = False
            else:
                pass
        if not idle:
            Ti = None
            # Run time TI to pass by reference.
            for T in TT:
                if Ti == None:
                    Ti = T
                elif T.deadline < Ti.deadline:
                    Ti = T
            schedule[t]=Ti
            Ti.duration -=1

        print(f"{schedule}")


        # if T.duraction == 0:
        #     for i in T:
        #
        #     else:
        #         t+=T.duration

        t += 5

        print(f"{wcrt}")
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    schedule()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
