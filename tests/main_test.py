import sys
import os
# this adds the main folder into this test scope so it will run as if in root
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/."))

import main
import libraries as libs
from unittest import TestCase

rel_path = os.path.realpath(os.path.dirname(__file__))


class MainTest(TestCase):
    def test_successful_scheduling_of_two_TT(self):
        inputTasks = libs.CSVReader.get_tasks(f'{rel_path}/../resources/test/data/tasks1.txt', 'TT')

        schedule, WRCT = libs.AlgoOne.scheduling_TT(inputTasks)

        # libs.Functions.printSchedule(schedule)

        # First task should be tTTO with earliest deadline
        self.assertEqual('tTT0', schedule[0].name)
        self.assertEqual(2000, schedule[0].deadline)
        self.assertEqual(55, schedule[0].computation)
        self.assertEqual('tTT0', schedule[54].name)
        self.assertEqual(1, schedule[54].computation)

        # Second task should be tTT1 with earliest deadline
        self.assertEqual('tTT1', schedule[55].name)
        self.assertEqual(45, schedule[55].computation)
        self.assertEqual(4000, schedule[55].deadline)
        self.assertEqual('tTT1', schedule[99].name)
        self.assertEqual(1, schedule[99].computation)

        # No task should be executed between 100 and 1999 based on their periods
        self.assertEqual('idle', schedule[100].name)
        self.assertEqual('idle', schedule[999].name)
        self.assertEqual('idle', schedule[1999].name)

        # At 2000 is the time to execute again tTTO based in its period
        self.assertEqual('tTT0', schedule[2000].name)
        self.assertEqual(4000, schedule[2000].deadline)
        self.assertEqual(55, schedule[2000].computation)
        self.assertEqual('tTT0', schedule[2054].name)
        self.assertEqual(1, schedule[2054].computation)

        # No task should be executed between 2055 and 3999 based on their periods
        self.assertEqual('idle', schedule[2055].name)
        self.assertEqual('idle', schedule[3999].name)

        # The lcm and should be the total array size (time)
        self.assertEqual(len(schedule), libs.Functions.lcm(inputTasks))

    def test_successful_scheduling_of_three_TT(self):
        inputTasks = libs.CSVReader.get_tasks(f'{rel_path}/../resources/test/data/tasks2.txt', 'TT')

        schedule, WRCT = libs.AlgoOne.scheduling_TT(inputTasks)

        # libs.Functions.printSchedule(schedule)

        # First task should be tTTO with earliest deadline
        self.assertEqual('tTT0', schedule[0].name)
        self.assertEqual(3000, schedule[0].deadline)
        self.assertEqual(55, schedule[0].computation)
        self.assertEqual('tTT0', schedule[54].name)
        self.assertEqual(1, schedule[54].computation)

        # Second task should be tTT2 with earliest deadline
        self.assertEqual('tTT2', schedule[55].name)
        self.assertEqual(45, schedule[55].computation)
        self.assertEqual(3000, schedule[55].deadline)
        self.assertEqual('tTT2', schedule[99].name)
        self.assertEqual(1, schedule[99].computation)

        # Third task should be tTT0 with earliest deadline
        self.assertEqual('tTT1', schedule[100].name)
        self.assertEqual(13, schedule[100].computation)
        self.assertEqual(4000, schedule[100].deadline)
        self.assertEqual('tTT1', schedule[112].name)
        self.assertEqual(1, schedule[112].computation)

        # No task should be executed between 113 and 3999 based on their periods
        self.assertEqual('idle', schedule[113].name)
        self.assertEqual('idle', schedule[1999].name)
        self.assertEqual('idle', schedule[2999].name)

        # At 3000 is the time to execute again tTT0 based in its period
        self.assertEqual('tTT0', schedule[3000].name)
        self.assertEqual(6000, schedule[3000].deadline)
        self.assertEqual(55, schedule[3000].computation)
        self.assertEqual('tTT0', schedule[3054].name)
        self.assertEqual(1, schedule[3054].computation)

        # Right after tTT0, the tTT2 should be executed since it is after 3000(period) before deadline(6000)
        self.assertEqual('tTT2', schedule[3055].name)
        self.assertEqual(45, schedule[3055].computation)
        self.assertEqual(6000, schedule[3055].deadline)
        self.assertEqual('tTT2', schedule[3099].name)
        self.assertEqual(1, schedule[3099].computation)

        self.assertEqual('idle', schedule[3199].name)
        self.assertEqual('idle', schedule[3999].name)

        # At 4000 is the time to execute again tTT1 based in its period
        self.assertEqual('tTT1', schedule[4000].name)
        self.assertEqual(8000, schedule[4000].deadline)
        self.assertEqual(13, schedule[4000].computation)
        self.assertEqual('tTT1', schedule[4012].name)
        self.assertEqual(1, schedule[4012].computation)

        # The lcm and should be the total array size (time)
        self.assertEqual(len(schedule), libs.Functions.lcm(inputTasks))

    def test_successful_scheduling_of_two_ET(self):
        # Event tasks to be scheduled by polling task
        inputTasksET = libs.CSVReader.get_tasks(f'{rel_path}/../resources/test/data/tasks3.txt', 'ET')
        self.assertEqual('tET0', inputTasksET[0].name)

        inputTasksTT = libs.CSVReader.get_tasks(f'{rel_path}/../resources/test/data/tasks3.txt', 'TT')
        self.assertEqual('tTT1', inputTasksTT[0].name)

        # Demo of how we will integrate it to the scheduling_TT based on given pdf hints
        lcm = libs.Functions.lcm(inputTasksTT)
        period = libs.Functions.get_polling_task_period(lcm)
        deadline = period
        results = [False, 900000000]
        # Hill climbing from 1 till period of server
        bestBudget = 0
        attemptsDuringPlateau = 3
        for budget in range(1, period):
            pollingTask = [budget, period, deadline]
            schedulable, responseTime = libs.AlgoTwo.scheduling_ET(pollingTask[0], pollingTask[1], pollingTask[2], inputTasksET)

            # if it is schedulable for budget then store responseTime if it's best found
            if (schedulable == True and responseTime <= results[1]):
                print('successful period:', budget)
                results[0] = True
                results[1] = responseTime

                if responseTime == results[1]:
                    attemptsDuringPlateau -= 1

                if attemptsDuringPlateau < 1:
                    break
                bestBudget = budget

        self.assertTrue(results[0])

    def test_successful_adding_polling_tasks_in_TT(self):
        # Event tasks to be scheduled by polling task
        inputTasksET = libs.CSVReader.get_tasks(f'{rel_path}/../resources/test/data/tasks4.txt', 'ET')
        inputTasksTT = libs.CSVReader.get_tasks(f'{rel_path}/../resources/test/data/tasks4.txt', 'TT')

        PTs = 3
        TT_and_PT, ET_WCRT, PT_created = libs.PollingServer.add_PT(inputTasksTT, inputTasksET, PTs)

        amountPT = 0
        for task in TT_and_PT:
            print(task.type)
            if task.type == 'PT':
                amountPT += 1
                print(task.separation)
                self.assertTrue(task.separation in [0, 1, 2, 3])

        self.assertEqual(PTs, amountPT)
        self.assertEqual(PTs, PT_created)

    def test_schedule_is_successfully_not_affected_by_task_list_without_ET(self):
        csv = f'{rel_path}/../resources/test/data/tasks1.txt' # no event tasks = no polling tasks
        TT, ET = main.get_tasks_from_csv(csv)
        solution = libs.Solution.schedule(TT, ET)

        schedule = solution.schedule

        # First task should be tTTO with earliest deadline
        self.assertEqual('tTT0', schedule[0].name)
        self.assertEqual(2000, schedule[0].deadline)
        self.assertEqual(55, schedule[0].computation)
        self.assertEqual('tTT0', schedule[54].name)
        self.assertEqual(1, schedule[54].computation)

        # Second task should be tTT1 with earliest deadline
        self.assertEqual('tTT1', schedule[55].name)
        self.assertEqual(45, schedule[55].computation)
        self.assertEqual(4000, schedule[55].deadline)
        self.assertEqual('tTT1', schedule[99].name)
        self.assertEqual(1, schedule[99].computation)

        # No task should be executed between 100 and 1999 based on their periods
        self.assertEqual('idle', schedule[100].name)
        self.assertEqual('idle', schedule[999].name)
        self.assertEqual('idle', schedule[1999].name)

        # At 2000 is the time to execute again tTTO based in its period
        self.assertEqual('tTT0', schedule[2000].name)
        self.assertEqual(4000, schedule[2000].deadline)
        self.assertEqual(55, schedule[2000].computation)
        self.assertEqual('tTT0', schedule[2054].name)
        self.assertEqual(1, schedule[2054].computation)

        # No task should be executed between 2055 and 3999 based on their periods
        self.assertEqual('idle', schedule[2055].name)
        self.assertEqual('idle', schedule[3999].name)

    def test_successful_scheduling_of_TT_and_one_PT(self):
        csv = f'{rel_path}/../resources/test/data/tasks5.txt'
        TT, ET = main.get_tasks_from_csv(csv)
        solution = libs.Solution.schedule(TT, ET)

        self.assertEqual(1, solution.PT_created)
        self.assertNotEqual(0, solution.cost)
