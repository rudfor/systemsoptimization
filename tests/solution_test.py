import sys
import os
# this adds the main folder into this test scope so it will run as if in root
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/."))

#import main
import libraries as libs
from unittest import TestCase

rel_path = os.path.realpath(os.path.dirname(__file__))

class SolutionTest(TestCase):
    def test_schedule_is_successfully_not_affected_by_task_list_without_ET(self):
        csv = f'{rel_path}/../resources/test/data/tasks1.txt' # no event tasks = no polling tasks
        TT, ET = libs.CSVReader.get_tasks_from_csv(csv)
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
        TT, ET = libs.CSVReader.get_tasks_from_csv(csv)
        solution = libs.Solution.schedule(TT, ET)

        self.assertEqual(1, solution.PT_created)
        self.assertNotEqual(0, solution.cost)
