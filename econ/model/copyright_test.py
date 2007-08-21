# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

import unittest
import random
import math

from econ.model.copyright import *
from econ.model.discount import *

class TestCopyrightIncome:

    def assertAlmostEqual(self, x, y):
        assert round(x-y,5) == 0
    
    def testCopyrightIncomeModelLinear(self):
        # get the std linear model of form a + bt with b = 0, a = 1
        a1 = 1
        incModel = CopyrightIncomeModelLinear()
        incModel.constant = a1
        
        assert incModel.getIncome(random.randint(0, 2000)) == a1
    
    def testCopyrightIncomeModelQuadratic(self):
        # - x (x - b) = - (x^2 - bx)
        b = random.randint(0, 100)
        quad1 = CopyrightIncomeModelQuadratic([0, b, -1])
        self.assertAlmostEqual(0, quad1.getIncome(b))
    
    def testExponentialModel(self):
        exponentialModel = CopyrightIncomeModelExponential()
        self.assertAlmostEqual(0.00673794699909, exponentialModel.getIncome(5))
    
    def testHybridModel(self):
        linearModel = CopyrightIncomeModelLinear()
        exponentialModel = CopyrightIncomeModelExponential()
        incomeModel = CopyrightIncomeModelHybrid()
        
        assert 0 == incomeModel.getIncome(10)
        
        incomeModel.getModelList().append((1, linearModel))
        incomeModel.getModelList().append((5, exponentialModel))
        smallNumber = 0.2
        largeNumber = 100
        assert 1 != incomeModel.getIncome(smallNumber)
        self.assertAlmostEqual(1, incomeModel.getIncome(largeNumber))
    
    def testSummary(self):
        drc1 = DiscountRateConstant()
        # set a 2% interest rate
        dr1 = 1/1.02
        drc1.setUnitDiscountRate(dr1)
        
        # get the std linear model of form a + bt with b = 0, a = 1
        # this has an analytic solution
        a1 = 1
        incModel = CopyrightIncomeModelLinear()
        incModel.constant = a1
        
        def linearSolution(constant, discount, period):
            return (1 - pow(discount, period)) / (1 - discount)
        def linearSolutionTotal(constant, discount):
            return 1 / (1 - discount)
        def numPeriods(proportion, discount):
            """
            Get number of periods necessary to obtain proportion of total
            **possible** income.
            proportion in [0,1)
            """
            return math.log(1 - proportion) / math.log(discount)
        def proportionOfTotalIncome(discount, numPeriods):
            return 1 - pow(discount, numPeriods)
        
        cis1 = CopyrightIncomeSummary(incModel, drc1)
        cis1.calculate()
        diff = cis1.totalPossibleIncome - linearSolutionTotal(a1, dr1)
        assert round(diff, 1) == 0
        
        ran2 = random.randint(0,1500)
        diff = cis1.getProportionOfTotalPossibleIncome(ran2) - proportionOfTotalIncome(dr1, ran2)
        assert round(diff, 1) == 0
