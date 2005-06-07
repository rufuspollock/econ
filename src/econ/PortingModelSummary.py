import pylab
from scipy import *

from econ.NetworkEffectsModel import *
from econ import plot_help
from econ.HtmlTableWriter import *

class PortingModelSummary:
    
    def __init__(self):
        """
        ownFixedCost = fixedCostConstant + beta
        portingCost = beta + beta0 * fixedCostConstant
        
        When beta = 0, portingCost / ownFixedCost = beta0
        """
        aa = 1.0
        bb = 10 * aa
        # power for het
        alpha = 10
        fixedCostConstant = 1.5
        beta0 = (2.0 / 3.0) * fixedCostConstant
        self.initialBeta = 0.0
        
        def nu1_A(tindex, beta, beta0):
            return - aa * math.sqrt((fixedCostConstant) / tindex)
        def nu1_B(tindex, beta, beta0):
            return - aa * math.sqrt((beta0  + beta) / (1 - tindex))
        
        def het1_A(tindex, *args):
            return - bb * (tindex ** alpha)
        def het1_B(tindex, *args):
            return het1_A(1-tindex)
        
        def priceFunction_A(price, *args):
            return -price
        def priceFunction_B(price, *args):
            return  priceFunction_A(price)
        
        self.neModel1 = NetworkEffectsModel(nu1_A, nu1_B,
                                            het1_A, het1_B,
                                            priceFunction_A, priceFunction_B,
                                            [self.initialBeta, beta0])
        self.startSearch = 0.67
        self.endSearch = 0.95
        self.startBeta = 0.0
        self.endBeta = 1.4
    
    def costFunction(self, betaValue):
        """
        Old value for original model is 0.1 beta ** 2
        """
        return 2.0 * betaValue ** 4
    
    def setBeta(self, betaValue):
        # beta variable index is 0
        self.neModel1.setConstant(0, betaValue)
    
    def profitFunction(self, betaValue):
        self.setBeta(betaValue)
        netProfits = self.neModel1.solveMonopolistPriceProblem(
            self.startSearch, self.endSearch)[2] \
            - self.costFunction(betaValue)
        return netProfits
    
    def getOptimalBeta(self):
        """
        Find the optimal beta for monopolist (prices are changeable as well)
        [[TODO: currently hard code where we search for beta. Need to be
        careful not to have beta too high or won't have any solutions ...]]
        """
        def tmpFunc(betaValue):
            return - self.profitFunction(betaValue)
        return optimize.fminbound(tmpFunc, self.startBeta, self.endBeta)
    
    def calculateWelfare(self):
        """
        Calculate welfare at 3 points:
            1. beta at initial value, prices at initial values
            (no monopoly pricing)
            2. beta at monopoly value, prices at initial value
            3. beta at initial value, monopoly price on A
            4. beta at monopoly value, monopoly price
            
        Record for each: beta, price on A, demand, net profits,
            consumer welfare, total welfare = consumer welfare + net profits 
        """
        monopolyBeta = self.getOptimalBeta()
        betaList = [self.initialBeta, monopolyBeta]
        initialPriceA = 0
        results = []
        for betaValue in betaList:
            self.setBeta(betaValue)
            self.neModel1.setPriceA(initialPriceA)
            eq1 = self.neModel1.getEquilibrium(self.startSearch,
                                                self.endSearch)
            consumerWelfare = self.neModel1.getConsumerWelfare(eq1)
            # no producer profits so welfare is just consumer welfare
            results.append([betaValue,
                            initialPriceA,
                            eq1,
                            0,
                            consumerWelfare, consumerWelfare])
        for betaValue in betaList:
            self.setBeta(betaValue)
            # demand is also the equilibrium value ...
            (monopolyPrice, demand, grossProfits) = \
                self.neModel1.solveMonopolistPriceProblem(0.6, 0.9)
            netProfits = grossProfits - self.costFunction(betaValue)
            self.neModel1.setPriceA(monopolyPrice)
            consumerWelfare = self.neModel1.getConsumerWelfare(demand)
            results.append([betaValue,
                            monopolyPrice,
                            demand,
                            netProfits,
                            consumerWelfare,
                            consumerWelfare + netProfits])
        
        writer1 = HtmlTableWriter()
        writer1.doPrettyPrint = False
        writer1.decimalPlaces = 3
        caption = 'Welfare Results at Various Prices and Fixed Costs (Beta)'
        headings = ['Beta',
                    'Price of A Hardware',
                    'Demand for A (market share)',
                    'Net Profits for M',
                    'Consumer Welfare',
                    'Total Welfare']
        rowHeadings = ['Beta at initial value, prices at initial value',
            'Beta at monopoly value, prices at initial value',
            'Beta at initial value, monopoly price on A',
            'Beta at monopoly value, monopoly price on A']
        return writer1.writeTable(results, caption, headings, rowHeadings)
    
    def plotProfitFunction(self):
        """
        Let f(t) be equilibriumFunction. Find a < b < c s.t. f(a), f(c) < 0
            and f(b) > 0
             ~~/\~~
         /_______\____ f(t) = 0
        /         \
         e1 emax e2
        
        1. find zeroes e1, e2.
        2. find emax = minimum demand locally,
            f(emax) = max possible price locally
        """
        aa = 0.4
        bb = 0.7
        cc = 0.9
        eps = 0.001
        equilLow = self.neModel1.getEquilibrium(aa,bb)
        equilHigh = self.neModel1.getEquilibrium(bb,cc)
        prices = arange(0.0, 0.25, 0.005)
        def demandFunction(tmpPrice):
            return self.neModel1.getDemand(tmpPrice, equilLow + eps, equilHigh + eps)
        def profitFunction(tmpPrice):
            return self.neModel1.getDemand(tmpPrice,
                equilLow + eps, equilHigh + eps) * tmpPrice
        demandSeries = plot_help.seriesMaker(prices,
            demandFunction, 'Demand Function Faced By Monopolist')
        profitSeries = plot_help.seriesMaker(prices,
            profitFunction, 'Profit Function of Monopolist')
        # plot_help.plotAssistant([demandSeries])
        plot_help.plotAssistant([profitSeries],
            'Monopoly Profits as a Function of Prices', 'Price', 'Profits')
        pylab.legend(loc = 'upper left')
    
    def plotProfitFunctionForPorting(self):
        """
        Plot profits as a function of beta
        """
        variableValues = arange(self.startBeta, self.endBeta,
            (self.endBeta - self.startBeta) / 50)
        series4 = plot_help.seriesMaker(variableValues,
            self.profitFunction, 'Profits for Platform A')
        # change so we don't write over any other figure
        pylab.figure(3)
        plot_help.plotAssistant([series4], 'Profits as Beta Varies', 'Beta',
            'Profits')
    
    def plotBetaSummary(self):
        betaValues = [0.4, 0.8, 1.2, 1.6, 2.0, 2.4]
        size = len(betaValues)
        for ii in range(size):
            subplotConfig = size * 100 + 10 + ii + 1
            pylab.subplot(subplotConfig)
            self.setBeta(betaValues[ii])
            self._plotSummary(self.neModel1, 0.45, 0.95)
            pylab.grid(1)
            pylab.xticks(arange(0.4,1.0,0.1))
            pylab.legend(loc = 'upper left')
    
    def makeSummaryGraph(self, betaValue = 0):
        self.setBeta(betaValue)
        self._plotSummary(self.neModel1, 0.45, 0.95)
        pylab.grid(1)
        pylab.xticks(arange(0.4,1.0,0.1))
        pylab.legend(loc = 'upper left')
        pylab.title('Summary Plot (Beta = ' + str(betaValue) + ')') 
        pylab.xlabel('Network share of A/Index of a consumer (t)')
    
    def _plotSummary(self, networkEffectsModel, start = 0.05, end = 0.95):
        eps = 0.05
        step = (end - start) / 50
        xvals = arange(start, end + step, step)
        def tmpFunc(tindex):
            return - networkEffectsModel.heterogeneityDisadvantage(tindex)
        
        series1 = plot_help.seriesMaker(xvals,
            networkEffectsModel.equilibriaFunction,
            'utility of A - utility of B')
        series2 = plot_help.seriesMaker(xvals,
            networkEffectsModel.networkAdvantage, 'network advantage')
        series3 = plot_help.seriesMaker(xvals,
            tmpFunc, 'heterogeneity disadvantage')
        plot_help.plotAssistant([series1, series2, series3])
