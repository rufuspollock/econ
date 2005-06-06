# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

class DemandFunction:
    
    def getDemand(self, price):
        pass

class DemandFunctionFromFunction:
    
    def __init__(self, demandFunction):
        self._demandFunction = demandFunction
    
    def getDemand(self, price):
        return self._demandFunction(price)