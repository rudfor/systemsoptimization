import main
import libraries as libs
from unittest import TestCase

class MainTest(TestCase):

    def test_simple(self):
        inputTasks = libs.CSVReader.get_tasks('../resources/Test/data/tasks1.txt', 'TT')

        schedule, WRCT = main.schedule(inputTasks, [])
        libs.Functions.printSchedule(schedule)
        self.assertIsNotNone(3)

    def test_simple_three_tasks(self):
        inputTasks = libs.CSVReader.get_tasks('../resources/Test/data/tasks2.txt', 'TT')

        schedule, WRCT = main.schedule(inputTasks, [])
        libs.Functions.printSchedule(schedule)
        self.assertIsNotNone(3)
