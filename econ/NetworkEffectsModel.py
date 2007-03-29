# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

# Reference for a) notation b) algorithms, as well as general companion is:
# [1] A Model of Porting with Special Attention to Microsoft v2, 2005
# Available from http://www.thefactz.org/economics/

import math
# optimize etc
from scipy import *

import econ.log
logger = econ.log.get_logger()

class NetworkEffectsModel:
    """
    Class both contains model information and provides helper functions to find
    e.g. equilibria.
    For notation and essential background reading see:
    [1] A Model of Porting; Pollock, R; 2005
        * http://www.thefactz.org/economics/
    This class and its algorithms is derived directly from that paper
    
    [[TODO: throughout we have problems when multiple equilibria since either:
        a. don't know which one the numerical search will use (and this messes 
        up other stuff that depends on it such as profit maximization
        b. have to provide bounds within which to search which give only one
        equilibria]]
    """
    
    def __init__(self, nu_A, nu_B, het_A, het_B, priceFunction_A,
        priceFunction_B, constantList = []):
        """
        Create Model using the supplied functions and variable list.
        (See [1] for more details)
        
        Comments
        ========
        1. It is required that one deal with arbitrary functional forms for
        network effect and heterogeneity. This means that we also need to deal
        with arbitrary set of variables hence the constantList parameter
        2. There are 2 platforms A,B
        3. Measure of consumers if 1 and they are indexed by t. This index is
        assumed to be the first argument for heterogeneity functions.
        4. Network effect first argument should be network size.
        
        @param nu_A: Network effect function for platform A
        @param nu_B: Network effect function for platform B (as a function of 
            network A size)
        @param het_A: Heterogeneity function for network A
        @param het_A: Heterogeneity function for network B
        @param: priceFunction_A: these are independent of index and dependent
        only on the platform chosen
        @param: constantList: arbitrary set of parameters passed to all functions
        """
        self._price_A = 0.0
        self._price_B = 0.0
        self._constantList = constantList
        
        # network effects on A and B (with extra parameters suppressed)
        def nuAtmp(networkSize):
            return apply(nu_A, [networkSize] + self._constantList)
        def nuBtmp(networkSize):
            return apply(nu_B, [networkSize] + self._constantList)
        
        # heterogeneity on A and B
        def hetAtmp(tindex):
            return apply(het_A, [tindex] + self._constantList)
        def hetBtmp(tindex):
            return apply(het_B, [tindex] + self._constantList)
        
        self._nu_A = nuAtmp
        self._nu_B = nuBtmp
        self._het_A = hetAtmp
        self._het_B = hetBtmp
        
        def priceFunctionATmp(priceTmp):
            return apply(priceFunction_A, [priceTmp] + self._constantList)
        
        def priceFunctionBTmp(priceTmp):
            return apply(priceFunction_B, [priceTmp] + self._constantList)
        
        self._priceFunction_A = priceFunctionATmp
        self._priceFunction_B = priceFunctionBTmp
        
        def tmpFunc1(tindex):
            return self._nu_A(tindex) - self._nu_B(tindex)
        def tmpFunc2(tindex):
            return self._het_A(tindex) - self._het_B(tindex)
        
        # advantage and disadvantage are with respect to network A
        self.networkAdvantage = tmpFunc1
        self.heterogeneityDisadvantage = tmpFunc2
    
    def equilibriaFunction(self, tindex):
        """
        A(t) (for defn of A(t) see [1])
        Interior equilibria are zeroes of utility_A = utility_B and therefore
        equilibria [1]
        @param tindex: t in A(t)
        @return: A(tindex)
        """
        return self.networkAdvantage(tindex) \
            + self.heterogeneityDisadvantage(tindex) \
            + self._priceFunction_A(self._price_A) \
            + self._priceFunction_B(self._price_B) \
    
    def getNuA(self):
        return self._nu_A
    
    def getNuB(self):
        return self._nu_B
    
    def getHetA(self):
        return self._het_A
    
    def getHetB(self):
        return self._het_B
    
    def getPriceFunctionA(self):
        return self._priceFunction_A
    
    def getPriceFunctionB(self):
        return self._priceFunction_B
    
    def setConstant(self, index, value):
        """Set constant with @param{index} in constantList to @param{value}."""
        self._constantList[index] = value
    
    def setPriceA(self, price):
        self._price_A = price
    
    def getEquilibrium(self, a, b):
        """
        Find an equilibrium in [a,b]
        @param a: see @param{b}
        @param b: we search for solutions in [a,b]
        @return: equilibrium of the model in [a,b]
        """
        fa = self.equilibriaFunction(a)
        fb = self.equilibriaFunction(b)
        if (fa > 0 and fb > 0) or (fa < 0 and fb < 0):
            tmsg = '(a,b,f(a),f(b)=' + str((a,b,fa,fb))
            tmsg += '\n\tA price:' + str(self._price_A)
            tmsg += '\n\tConstants:' + str(self._constantList)
            logger.info(tmsg)
        return optimize.bisect(self.equilibriaFunction, a, b)
    
    def getDemand(self, price, startSearch, endSearch):
        """
        Get demand for platform A at given given price.
        Simplest solution would to solve
            g(t) - f(p) = 0
        Where g(t) is equilibria function with p = 0 and g(p) is price function
        Problems:
            1. No solution
            2. Multiple solutions
        Currently user specifies an area [startSearch, endSearch] to search in
        which there is one and only one equilibrium.
        Then find
            1. local equilibrium t1
            2. local maximum of g(t) at t2 (for stable equlibrium can assume
            t2 < t1) 
        So search in [t2, t1]
        
        [[TODO:? deal with unstable case or warn about it]]
        @param price: price of platform A
        @param startSearch: [startSearch, endSearch] is an area in which to
            search for equilibrium in which there is one and only one
            equilibrium.
        @param endSearch: [startSearch, endSearch] is an area in which to
            search for equilibrium in which there is one and only one
            equilibrium.
        """
        (maximalPrice, boundaryDemand) = self._findMaximalAllowablePrice(
            startSearch, endSearch)
        logger.debug('Maximal allowable price:' + str(maximalPrice))
        # if price too high no local solution for that demand so return
        # -ve demand
        if price > maximalPrice:
            logger.info('getDemand: price (' + str(price) +
                ') exceeeded maximal price (' +
                str(maximalPrice) + '). Returning demand of 0')
            return 0
        # solve g(t) = f(p) for t
        self._price_A = price
        demand = self.getEquilibrium(boundaryDemand, endSearch)
        return demand
    
    def _findMaximalAllowablePrice(self, startSearch, endSearch):
        """
        Find (locally) maximal price that can be charged before getting
        discontinuity in demand.
        See getDemand for more information on parameters.
        """
        self._price_A = 0
        def tmpFunc(xx):
            return - self.equilibriaFunction(xx)
        # this is lowest demand can go if it is coming from shifting equilibrium function down
        boundaryDemand = optimize.fminbound(tmpFunc, startSearch, endSearch)
        # [[TODO: do inverse of price function rather than assume linear constant price function so that price is just f(result)]]
        maximalPrice = self.equilibriaFunction(boundaryDemand)
        return (maximalPrice, boundaryDemand)
    
    def solveMonopolistPriceProblem(self, startSearch, endSearch):
        """
        Get profits for monopolist on platform A by solving the profit
        maximization problem.
        
        @param startSearch: see @param{endSearch}
        @param endSearch: define interval [startSearch, endSearch] in which to
            search when inverting equilibrium function to find demand
        @return tuple (maximizing price, demand, profits = price * demand)
        """
        (maximalPrice, tmp1) = self._findMaximalAllowablePrice(startSearch,
                                                                    endSearch)
        # need negative of profits as solver searches for minimum
        def profitFunction(price):
            return - self.getDemand(price, startSearch, endSearch) * price
        maximizingPrice = optimize.fminbound(profitFunction, 0, maximalPrice)
        demand = self.getDemand(maximizingPrice, startSearch, endSearch)
        return (maximizingPrice, demand, maximizingPrice * demand)
    
    def getConsumerWelfare(self, equilibriumValue):
        """
        Calculate total consumer welfare
            W = \int_{A} u(t,A) dt +\int_{B} u(t,B) dt.
        Can break this up as:
        W = Network Effect Benefits + Heterogeneity Stuff
        W = t^{e} * \nu(t^{e}, A) + (1-t^{e}) * \nu(1-t^{e}) + Heterogeneity
        NB: we are assuming demand has been normalized to 1
        
        @param equilibriumValue: the equilibrium to use when calculating social welfare
        @return: total consumer welfare
        """
        networkAPart = equilibriumValue * self._nu_A(equilibriumValue)
        # Remember _nu_B defined a function of network A size ...
        networkBPart = (1.0 - equilibriumValue) * \
            self._nu_B(equilibriumValue)
        
        hetAPart = integrate.quad(self._het_A, 0, equilibriumValue)[0]
        hetBPart = integrate.quad(self._het_B, equilibriumValue, 1)[0]
        
        priceAPart = equilibriumValue * self._priceFunction_A(self._price_A)
        priceBPart = equilibriumValue * self._priceFunction_B(self._price_B)
        
        logger.debug('Welfare: (netA, netB, hetA, hetB): ' + \
            str((networkAPart, networkBPart, hetAPart, hetBPart)))
        totalWelfare = (networkAPart + networkBPart +
                        hetAPart + hetBPart + priceAPart + priceBPart)
        return totalWelfare
