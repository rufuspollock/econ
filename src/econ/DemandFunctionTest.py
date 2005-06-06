# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

import unittest
import random

from DemandFunction import *

class DemandFunctionTest(unittest.TestCase):
    
    def test1(self):
        alpha = -1.0
        kk = 1.0
        def demandFunction(price):
            return kk * price ** alpha
        
        df1 = DemandFunctionFromFunction(demandFunction)
        inPrice1 = random.random() * 5000
        expDemand1 = demandFunction(inPrice1)
        outDemand1 = df1.getDemand(inPrice1)
        self.assertEqual(expDemand1, outDemand1,
            'Expected demand and actual demand are not equal')