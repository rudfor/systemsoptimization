import main
import libraries as libs
from unittest import TestCase

class MainTest(TestCase):

    def test_simple(self):
        inputTasks = libs.CSVReader.get_tasks('../resources/Test/data/tasks1.txt', 'TT')

        schedule, WRCT = main.schedule(inputTasks, [])
        self.assertIsNotNone(3)
