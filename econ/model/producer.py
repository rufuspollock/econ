"""
Copyright (c) 2005, Rufus Pollock. All Rights Reserved
See the LICENSE file in the distribution root for licensing details

Models from Producer theory
"""

# importing for cgi this bombs out on importing of scipy_base._compiled_base.so
# via: scipy_base.__init__.py, scipy_base/index_tricks.py,
# scipy_base.function_base.py
from scipy import integrate, optimize, derivative, arange
# don't import pylab here as introduces dependency on a lot of graphics stuff

class Producer(object):
    
    MAXPRICE = 10.0
    "Maximum value for price. Used extensively when solving numerically"
    
    def __init__(self, demandFunction, costFunction):
        self.demandFunction = demandFunction
        self.costFunction = costFunction
    
    def profitFunction(self, price):
        """
        Get profits for producer at this price.
        
        It is assumed that if profits would be negative at a particular price
        (and the associated demand) then the producer may choose to supply a
        zero amount -- note that this may still result in negative profits
        should there be fixed costs.
        """
        quantity = self.demandFunction(price)
        return max(self.costFunction(0),
                   price * quantity - self.costFunction(quantity))
    
    def getMonopolyPrice(self):
        """
        Usual global vs. local issues ...
        """
        startSearch = 0.0
        endSearch = self.MAXPRICE
        def tmpFunc(price):
            return - self.profitFunction(price)
        maxPrice = optimize.fminbound(tmpFunc, startSearch, endSearch)
        steps = 500
        eps = (endSearch - startSearch) / steps
        # may need to use brute rather than fminbound for robustness 
        # e.g. with fixed costs profit function is zero (with zero output) up
        # to some threshold.
        # just cannot get this to work ...
        # maxPrice, maxDemand = optimize.brute(tmpFunc, ((startSearch, endSearch,
        #    eps))
        #        )
        # maxPrice = optimize.fmin(tmpFunc, (startSearch - endSearch)/2.0)
        return maxPrice
    
    def getMonopolyProfits(self):
        return self.profitFunction(self.getMonopolyPrice())
    
    def getCompetitivePrice(self):
        """
        Solve c'(q(p)) = p
        
        Model situation with perfect competition where in equilibrium marginal
        profit is 0 (so marginal cost equals marginal revenue).
        
        NB: various assumptions required such as no increasing returns as well
        as that c' > 0
        """
        def marginalCost(quantity):
            return derivative(self.costFunction, quantity)
        def tmpFunc(price):
            return marginalCost(self.demandFunction(price)) - price
        # initialGuess should be non-zero so as to avoid problems with demand
        # functions that go to infinity there
        initialGuess = self.MAXPRICE / 2.0
        return optimize.fsolve(tmpFunc, initialGuess)
    
    def getMonopolyDeadweightCosts(self):
        """
        Compute the monopoly deadweight loss
        
          |~
          | \
          |-- \
        Q | |;;;\
          |------ \
          | |   |   \
          ------------>
              P
        
        """
        priceC = self.getCompetitivePrice()
        priceM = self.getMonopolyPrice()
        quantityC = self.demandFunction(priceC)
        quantityM = self.demandFunction(priceM)
        totalArea = integrate.quad(self.demandFunction, priceC, priceM)[0]
        return totalArea - ( (priceM - priceC) * quantityM )
    
class ProducerSummary(object):
    
    def __init__(self, producer):
        self._producer = producer
        self.eps = self._producer.MAXPRICE / 100.0
    
    def plotProfitFunction(self):
        """
        Plot the profit function for a given producer
        """
        import pylab
        print 'Starting this function'
        priceValues = arange(0.0, self._producer.MAXPRICE, self.eps)
        profitValues = [ self._producer.profitFunction(pp) for pp in
            priceValues ]
        pylab.plot(priceValues, profitValues)
        pylab.xlabel('Price')
        pylab.ylabel('Profits')
    
    def plotProducerSummary(self, minPrice = 0.0):
        """
        Plot demand function for producer with variables of interest such as
        monopoly price, competive price, deadweight loss etc.
        
        Plot in traditional manner with demand on x axis
        """
        import pylab
        prod = self._producer
        demandAxisOrigin = 0.0
        
        priceValues = arange(minPrice, self._producer.MAXPRICE, self.eps)
        demandValues = [ prod.demandFunction(price) for price in priceValues ]
        # fix zero division issues plus scale problems
        def avg_cost(quantity):
            if quantity == 0:
                return prod.MAXPRICE
            else:
                return min(prod.MAXPRICE, prod.costFunction(quantity)/quantity)
        avg_costs = [  avg_cost(dd) for dd in demandValues ]
        competitivePrice = prod.getCompetitivePrice()
        monopolyPrice = prod.getMonopolyPrice()
        monopoly_profits = prod.profitFunction(monopolyPrice)
        competitiveDemand = prod.demandFunction(competitivePrice)
        monopolyDemand = prod.demandFunction(monopolyPrice)
        dw_costs = prod.getMonopolyDeadweightCosts()
        # [[TODO what happens if this is infinite
        maxDemand = prod.demandFunction(minPrice)

        print 'Monopoly price: ', monopolyPrice
        print 'Monopoly demand: ', monopolyDemand
        print 'Monopoly profits: ', monopoly_profits
        print 'Deadweight losses: ', dw_costs
        
        fig = pylab.figure(1)
        pylab.plot(demandValues, priceValues, 'k')
        pylab.plot(demandValues, avg_costs, 'k--')
        pylab.xlabel('Quantity')
        pylab.ylabel('Price')
        pylab.axis(xmin=demandAxisOrigin)
        
        # this assumes demand axis origin starts at 0
        pylab.axhline(monopolyPrice, 0, monopolyDemand / maxDemand, color='k')
        pylab.axhline(competitivePrice, 0, competitiveDemand / maxDemand,
                color='k', linestyle='-.')
        pylab.axvline(monopolyDemand, 0, monopolyPrice / prod.MAXPRICE,
                color='k')
        # not sure we want this
        # pylab.axvline(competitiveDemand, 0, competitivePrice / maxDemand)
        
        newLocs = None
        newLabels = None
        def addTicks(ticks, extraTicks):
            """
            ticks is pylab.xticks of pylab.yticks
            Can only run once or screws up because labels don't get reused ..
            """
            locs, labels = ticks()
            newLocs = list(locs)
            newLabels = [ str(loc) for loc in locs]
            for extraTick in extraTicks:
                position = extraTick[0]
                extraLabel = extraTick[1]
                newLabel = str(position)[:3]
                if extraLabel != '': newLabel += '\n(%s)' % extraLabel
                newLocs.append(position)
                newLabels.append(newLabel)
            ticks(newLocs, newLabels)
        
        addTicks(pylab.xticks, [(competitiveDemand, 'qC'), (monopolyDemand, 'qM')])
        addTicks(pylab.yticks, [(competitivePrice, 'pC'), (monopolyPrice, 'pM')])
