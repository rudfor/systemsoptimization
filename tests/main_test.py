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
    def test_we_successfully_selected_the_best_proposed_solution(self):
        csv = f'{rel_path}/../resources/test/data/tasks6.txt'

        final_solution, all_SA_solutions = main.search_solution(csv)

        print('Best Selected Solution:', final_solution.cost, final_solution.PT_created)

        best = libs.SolutionModel([], 1000000, 0)
        for solution in all_SA_solutions:
            print('SA Proposed Solution:', solution.cost, solution.PT_created)
            if best.cost < solution.cost:
                best = solution

        self.assertEqual(1, final_solution.PT_created)
        self.assertNotEqual(0, final_solution.cost)
