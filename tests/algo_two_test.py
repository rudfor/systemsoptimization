import sys
import os
# this adds the main folder into this test scope so it will run as if in root
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/."))

import libraries as libs
from unittest import TestCase

rel_path = os.path.realpath(os.path.dirname(__file__))


class AlgoTwoTest(TestCase):
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
