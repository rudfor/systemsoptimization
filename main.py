#!/usr/bin/env python3

import libraries as libs

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Ask user for file input
    csv = input("CSV path file: ") or 'resources/tasks.txt'

    # Init scheduling
    solution = libs.Solution.search_solution(csv)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
