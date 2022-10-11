import main
import libraries as libs
from unittest import TestCase

class MainTest(TestCase):

    def test_simple(self):
        inputTasks = libs.CSVReader.get_tasks('../resources/Test/data/tasks1.txt', 'TT')

        schedule, WRCT = main.schedule(inputTasks, [])

        # libs.Functions.printSchedule(schedule)

        self.assertEqual('tTT0', schedule[0].name)
        self.assertEqual(2000, schedule[0].deadline)
        self.assertEqual(55, schedule[0].duration)
        self.assertEqual('tTT0', schedule[54].name)
        self.assertEqual(1, schedule[54].duration)

        self.assertEqual('tTT1', schedule[55].name)
        self.assertEqual(45, schedule[55].duration)
        self.assertEqual(4000, schedule[55].deadline)
        self.assertEqual('tTT1', schedule[99].name)
        self.assertEqual(1, schedule[99].duration)

        self.assertEqual('idle', schedule[100].name)
        self.assertEqual('idle', schedule[999].name)
        self.assertEqual('idle', schedule[1999].name)

        self.assertEqual('tTT0', schedule[2000].name)
        self.assertEqual(4000, schedule[2000].deadline)
        self.assertEqual(55, schedule[2000].duration)
        self.assertEqual('tTT0', schedule[2054].name)
        self.assertEqual(1, schedule[2054].duration)

        self.assertEqual('idle', schedule[2055].name)
        self.assertEqual('idle', schedule[3999].name)

        self.assertEqual(len(schedule), libs.Functions.lcm(inputTasks))


    def test_simple_three_tasks(self):
        inputTasks = libs.CSVReader.get_tasks('../resources/Test/data/tasks2.txt', 'TT')

        schedule, WRCT = main.schedule(inputTasks, [])

        # libs.Functions.printSchedule(schedule)

        self.assertEqual('tTT0', schedule[0].name)
        self.assertEqual(3000, schedule[0].deadline)
        self.assertEqual(55, schedule[0].duration)
        self.assertEqual('tTT0', schedule[54].name)
        self.assertEqual(1, schedule[54].duration)

        self.assertEqual('tTT2', schedule[55].name)
        self.assertEqual(45, schedule[55].duration)
        self.assertEqual(3000, schedule[55].deadline)
        self.assertEqual('tTT2', schedule[99].name)
        self.assertEqual(1, schedule[99].duration)

        self.assertEqual('tTT1', schedule[100].name)
        self.assertEqual(13, schedule[100].duration)
        self.assertEqual(4000, schedule[100].deadline)
        self.assertEqual('tTT1', schedule[112].name)
        self.assertEqual(1, schedule[112].duration)

        self.assertEqual('idle', schedule[113].name)
        self.assertEqual('idle', schedule[1999].name)
        self.assertEqual('idle', schedule[2999].name)
        self.assertEqual('idle', schedule[3999].name)

        self.assertEqual('tTT1', schedule[4000].name)
        self.assertEqual(8000, schedule[4000].deadline)
        self.assertEqual(13, schedule[4000].duration)
        self.assertEqual('tTT1', schedule[4012].name)
        self.assertEqual(1, schedule[4012].duration)

        self.assertEqual('idle', schedule[1999].name)
        self.assertEqual('idle', schedule[2999].name)

        self.assertEqual('tTT0', schedule[3000].name)
        self.assertEqual(6000, schedule[3000].deadline)
        self.assertEqual(55, schedule[3000].duration)
        self.assertEqual('tTT0', schedule[3054].name)
        self.assertEqual(1, schedule[3054].duration)

        self.assertEqual('tTT2', schedule[3055].name)
        self.assertEqual(45, schedule[3055].duration)
        self.assertEqual(6000, schedule[3055].deadline)
        self.assertEqual('tTT2', schedule[3099].name)
        self.assertEqual(1, schedule[3099].duration)

        self.assertEqual('idle', schedule[3100].name)

        self.assertEqual(len(schedule), libs.Functions.lcm(inputTasks))



