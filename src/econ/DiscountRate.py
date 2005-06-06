# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

# Calculate discount rates.
# Discount rates arise in relation to interest, inflation and utility
# These can be derived either from models or from empirical data

import logging
logger = logging.getLogger("econ")

class DiscountRate:
    """
    Interface class for model/empirical discount rates
    """
    
    def getDiscount(self, receiveTimePoint, evaluationTimePoint = 0):
        """
        Get rate of return between evaluationTimePoint and receiveTimePoint.
        That is value x s.t. 1 unit at receiveTimePoint yields x at evaluation time point
         
        For standard present value evaluationTimePoint = 0 and receiveTimePoint is in future
        For standard cumulation, e.g. interest rates, evaluationTimePoint follows receiveTimePoint
        """
        # might be worth not doing straightforward inheritance but rather using hook functions as that way we can do basic sanity checking in one place such as startPoint < endPoint here
        pass
    
    def getReturn(self, evaluationTimePoint, receiveTimePoint = 0):
        return (1/(self.getDiscount(evaluationTimePoint, receiveTimePoint)))

class DiscountRateConstant(DiscountRate):
    
    discountRate = 1
    # if true automatically assume rates above 1 are interest rates and convert accordingly 
    assumeRateAboveOneIsInterestRate = True
    
    def __init__(self, discountRate = 1):
        self.setUnitDiscountRate(discountRate)
    
    def getDiscount(self, receiveTimePoint, evaluationTimePoint = 0):
        logger.debug("DiscountRateConstant.getReturnRate(). evalTimePoint = " + str(evaluationTimePoint) + " receiveTimePoint = " + str(receiveTimePoint))
        logger.debug("(Unit) return rate: " + str(self.discountRate))
        return pow(self.discountRate, receiveTimePoint - evaluationTimePoint) 
    
    def setUnitDiscountRate(self, discountRate):
        self.discountRate = self.__processRateOnSetting(discountRate)
    
    def getUnitDiscountRate(self):
        return self.discountRate
        
    def __processRateOnSetting(self, rate):
        if self.assumeRateAboveOneIsInterestRate and (rate > 1):
            return 1.0/rate
        else:
            return rate

class InflationRate:
    pass
