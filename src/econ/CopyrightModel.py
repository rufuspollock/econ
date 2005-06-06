# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

# Some Terminology
# i(t) real income in period preceding t
# I(t) PV of total income to time T

import math

import logging
logger = logging.getLogger("econ")

## **************************************************************************
## Income Model Classes
## **************************************************************************

class CopyrightIncomeModel:
    """
    A model for i(t) (see above defn)
    Interface class that actual models will inherit from.
    """
    
    def getIncome(self, startDate, period = 1):
        """
        [[TODO: sort this out ]]
        Get income for a single time period finishing at endDate
        Assume income is adjusted so that it is as if a single lump sum
        were paid at endDate (so cumulate as necessary)
        """
        pass
        
class CopyrightIncomeModelLinear(CopyrightIncomeModel):
    def __init__(self, constant = 1):
        self._constant = constant
        self._slope = 0
    
    def getIncome(self, startDate, period = 1):
        return (max(0, startDate * self._slope + self._constant))/ period

class CopyrightIncomeModelExponential(CopyrightIncomeModel):
    
    def __init__(self, constant = 1, alpha = 1):
        """
        Negative exponential: constant * exp(- alpha * t)
        """
        self._constant = 1
        self._alpha = 1
        
    def getIncome(self, startDate, period = 1):
        # [[TODO: ?? test alpha is positive ...]]
        return max(0, self._constant * math.e**( - self._alpha * startDate))
    

class CopyrightIncomeModelQuadratic(CopyrightIncomeModel):
    
    def __init__(self, coeffs):
        self._coefficients = coeffs
    
    def getIncome(self, startDate, period = 1):
        return max(0, self._coefficients[0] + self._coefficients[1] * startDate + self._coefficients[2] * startDate * startDate)


class CopyrightIncomeModelHybrid(CopyrightIncomeModel):
    """
    A hybrid models consists of a linear sum of basic models. \sum_{i}^{n} k_{i} model_{i}
    
    NB: the one issue is that we re-impose >= 0 on the hybrid model even though this already done in the individual models to allow for possibility that constants of addition are negative
    """
    
    def __init__(self, modelList = []):
        """
        modelList will be a list of pairs consisting of (k, model) where k is composition constant
        """
        self._modelList = modelList
    
    def getIncome(self, startDate, period = 1):
        return max(0, self.__getLinearModelSum(startDate, period))
    
    def getModelList(self):
        return self._modelList
    
    def __getLinearModelSum(self, startDate, period):
        result = 0
        for item in self._modelList:
            result += item[0] * item[1].getIncome(startDate, period)
        return result

## **************************************************************************
## Summary Classes
## **************************************************************************

class CopyrightIncomeSummary:
    """
    Summarize information about copyright income
    Assume: that non-PV income is constant or declining eventually so as to
    assure theoretical and numerical convergence
    
    TODO: need to sort out threshold to be better
    """
    # max time period to calculate until in getting income
    # (to stop overrunning memory etc)
    maxTimePeriod = 1000
    minTimePeriod = 150
    
    # terminate income accumalation if period income PV is less than this
    incomeThreshold = 0.001
    
    def __init__(self, incomeModel, discountRate):
        """
        Initializes fundamentals and then calculates summary information
        """
        # do we delay income model by one period?
        self.firstPaymentDelay = 0
        # income stream at present value
        self.presentValueOfIncome = []
        self.cumulativeTotals = []
        self.discountRate = discountRate
        self.incomeModel = incomeModel
        self.calculate()
    
    def calculate(self):
        """
        Calculate summary information. Specifically:
            Calculate NPV of i(t)
            Calculate I(t)
            Calculate total possible income
        Results are stored in presentValueOfIncome
        Keeps running until PV of income being added is negligible or we reach
        maxTimePeriod
        """
        self.presentValueOfIncome = []
        self.cumulativeTotals = []
        total = 0
        # just define to anything > incomeThreshold
        incomePV = self.incomeThreshold + 1 
        ii = 0
        while incomePV > self.incomeThreshold or ii < self.minTimePeriod:
            incomePV = self.incomeModel.getIncome(ii) * \
                self.discountRate.getDiscount(ii + self.firstPaymentDelay)
            total += incomePV
            self.presentValueOfIncome.append(incomePV)
            self.cumulativeTotals.append(total)
            if ii > self.maxTimePeriod:
                # break out anyway
                logger.warning(
                    "Income PV was NOT below threshold after " +
                    str(self.maxTimePeriod) +
                    " periods. Income in current period was: " + (incomePV))
                break
            ii += 1
        logger.debug("number of iterations = "  + str(ii))
        logger.debug("PV of last period income = " + str(incomePV))
        # now make summaries
        self.totalPossibleIncome = total
    
    def getPresentValueOfIncome(self):
        return self.presentValueOfIncome
    
    def getCumulativeTotals(self):
        """Get the cumulative (PV) income totals"""
        return self.cumulativeTotals
    
    def getTotalPossibleIncome(self):
        return self.totalPossibleIncome
    
    def getProportions(self):
        """
        @return a list where entry i = proportion of total possible income
            earned by period i (i.e. I(i) / I(infty))
        """
        return [xx / self.totalPossibleIncome for xx in self.cumulativeTotals]
    
    def getProportionOfTotalPossibleIncome(self, numPeriods):
        if numPeriods > len(self.presentValueOfIncome):
            return 1
        else:
            return self.cumulativeTotals[numPeriods] / self.totalPossibleIncome
        
if __name__ == "__main__":
    incModel = CopyrightIncomeModelLinear()
    dr = DiscountRate()
    print incModel.getIncome(0)
    print dr.getPresentValue(10)
    print calculateIncome(incModel, 10)