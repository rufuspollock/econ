# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

import unittest
import random

from econ.model.demand import *

class TestDemandFunction:
    
    def testGetLinearDemandFunction(self):
        constant = 2.0
        slope = -1.0
        df1 = getLinearDemandFunction(constant, slope)
        price1 = random.random() * 3.0
        expDemand = max(0, 2.0 + price1 * slope)
        assert expDemand == df1(price1)
        
        
        
