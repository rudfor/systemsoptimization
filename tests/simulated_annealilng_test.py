import sys
import os
# this adds the main folder into this test scope so it will run as if in root
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/."))

#import main
import libraries as libs
from unittest import TestCase

rel_path = os.path.realpath(os.path.dirname(__file__))

class SimulatedAnnealingTest(TestCase):
    def test_simulated_annealing_finds_a_proposed_solution(self):
        csv = f'{rel_path}/../resources/test/data/tasks6.txt'
        TT, ET = libs.CSVReader.get_tasks_from_csv(csv)
        initial_solution = libs.Solution.schedule(TT, ET)

        suggested_solution = libs.simulated_annealing(initial_solution, TT, ET)

        print('SA Test Solution:', suggested_solution.cost, suggested_solution.PT_created)

        self.assertEqual(1, suggested_solution.PT_created)
        self.assertNotEqual(0, suggested_solution.cost)
