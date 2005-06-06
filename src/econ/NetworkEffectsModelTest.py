# Copyright (c) 2005, Rufus Pollock. All Rights Reserved
# Licensed under the GNU Public License (GPL) v2.0
# See the LICENSE file in the root of the distribution for details

import random
import unittest

from NetworkEffectsModel import *

class NetworkEffectsModelTest(unittest.TestCase):
    def __init__(self, methodName = 'testGetEquilibrium'):
        """
        Need this so that we can instantiate the class outside of test
        framework for use in graphing etc
        """
        super(NetworkEffectsModelTest, self).__init__(methodName)
    
    ## ********************************************************************
    ## Network Effect Models
    ## ********************************************************************
    
    def linearNetworkEffects(self, aa, bb1, bb2):
        """
        This implements the standard linear model
        Here as a demo and test case
        
        v(t) = aa * t
        h(A,t) = - bb1 * t
        h(B,t) = - bb2 * (1-t)
        """
        def nu1_A(tindex):
            return aa * tindex
        def nu1_B(tindex):
            return nu1_A(1-tindex)
        
        def het1_A(tindex):
            return - bb1 * tindex
        def het1_B(tindex):
            return - bb2 * (1-tindex)
        
        def priceFunction_A(price):
            return -price
        
        def priceFunction_B(price):
            return priceFunction_A(price)
            
        return NetworkEffectsModel(nu1_A, nu1_B, het1_A, het1_B,
            priceFunction_A, priceFunction_B)
    
    def locationalINESymmetric(self, aa, bb, alpha = 1.0):
        """
        Symmetric indirect network effects (based on locational model of
        imperfect competition) model
        
        main features of this model
        networks are symmetric in all features
        v(t) ~ aa * 1/sqrt(t)
        h(t) ~ bb * t^alpha
        priceFunction(p) = - priceScaleFactor * p
        """
        
        def nu1_A(tindex):
            return - aa * math.sqrt(1.0 / tindex)
        def nu1_B(tindex):
            return nu1_A(1-tindex)
        
        def het1_A(tindex):
            return - bb * (tindex ** alpha)
        def het1_B(tindex):
            return het1_A(1-tindex)
        
        def priceFunction_A(price):
            return - price
        
        def priceFunction_B(price):
            return  priceFunction_A(price)
        
        return NetworkEffectsModel(nu1_A, nu1_B, het1_A, het1_B,
            priceFunction_A, priceFunction_B)
    
    ## ********************************************************************
    ## Tests
    ## ********************************************************************
    
    def setUp(self):
        self._neModel1 = self.locationalINESymmetric(1, 5, 7)
        self._aa = 1.0
        self._bb1 = 2.0
        self._bb2 = 2.0
        self._linearModel = self.linearNetworkEffects(self._aa, self._bb1,
            self._bb2)
    
    def testGetNuA(self):
        nuA = self._linearModel.getNuA()
        def actualNuA(tt):
            return self._aa * tt
        tval = random.random()
        self.assertAlmostEqual(nuA(tval), actualNuA(tval))
    
    def testGetPriceFunctionA(self):
        pfA = self._linearModel.getPriceFunctionA()
        self.assertAlmostEqual(pfA(1.0), -1.0)
    
    def testGetPriceFunctionB(self):
        pfB = self._linearModel.getPriceFunctionB()
        self.assertAlmostEqual(pfB(1.0), -1.0)
    
    def testGetEquilibrium(self):
        # 1. test linear case
        # interior analytical soln
        analyticalSolution = (self._aa - self._bb2) / \
            (2 * self._aa - self._bb1 - self._bb2)
        out1 = self._linearModel.getEquilibrium(0.01, 0.99)
        self.assertAlmostEqual(out1, analyticalSolution)
        # 2. test locational case
        modelx = self._neModel1
        self.assertAlmostEqual(modelx.getEquilibrium(0.55, 0.9),0.821832850473)
    
    def testGetDemand(self):
        # demand function has form: q(p) = (a-bb2)/m + p/m
        # tmp1 = m = 2a - bb1 - bb2
        tmp1 = 2 * self._aa - self._bb1 - self._bb2
        def demandFunction(price):
            return (1.0/tmp1) * (self._aa - self._bb2 + price)
        maxPrice = -(self._aa - self._bb2) / (tmp1 ** 2)
        price = maxPrice * random.random()
        equilTmp = self._linearModel.getEquilibrium(0.0, 1.0)
        out1 = self._linearModel.getDemand(price, 0.0, equilTmp)
        self.assertAlmostEqual(out1, demandFunction(price), 7,
            'Error: price=' + str(price))
        
    def _plotDemand(self):
        """Useful helper for debugging"""
        import plot_help
        import pylab
        import scipy
        prices = scipy.arange(0.0, 1.0, 0.05)
        def demandFunction(priceTmp):
            return self._linearModel.getDemand(priceTmp, 0.0, equilTmp)
        series1 = plot_help.seriesMaker(prices, demandFunction)
        plot_help.plotAssistant([series1])
        pylab.show()
    
    def testGetConsumerWelfare(self):
        modelLinear = self._linearModel
        eq1 = modelLinear.getEquilibrium(0.01, 0.99)
        outWelfare = modelLinear.getConsumerWelfare(eq1)
        expectedWelfare = ( (self._aa - 0.5 * self._bb1) * eq1**2 +
            (self._aa - 0.5 * self._bb2) * (1-eq1)**2 )
        self.assertEqual(outWelfare, expectedWelfare)