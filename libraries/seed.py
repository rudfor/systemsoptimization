#!/usr/bin/env python3


class Seed:
    def __init__(self, schedule, cost, PT_created, schedulable = False):
        self.schedule = schedule
        self.cost = cost
        self.PT_created = PT_created
        self.schedulable = schedulable


class PollingServer:
    def __init__(self, ETs = []):
        self.et_list = ETs


if __name__ == '__main__':
    # Ask user for file input
    print(f'Do not run this Script Directly')
