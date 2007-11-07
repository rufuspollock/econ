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
    
    def __init__(self, demand_function, cost_function, max_price=20.0):
        '''
        @param max_price: maximum value for range of 'interesting' prices, that
        is range in which we will need to solve for variables of interest
        (e.g. monopoly price etc). Needed because we solve for many things
        numerically and need and upper bounds on zeroes, minima etc etc.
        '''
    
        self.demand_function = demand_function
        self.cost_function = cost_function
        # deal with zero demand function (since this messes up optimization)
        eps = 0.1
        check_price = max_price
        while(self.demand_function(check_price) == 0):
            check_price -= eps
        self.MAXPRICE = check_price + eps
    
    def profit_function(self, price):
        """
        Get profits for producer at this price.
        
        It is assumed that if profits would be negative at a particular price
        (and the associated demand) then the producer may choose to supply a
        zero amount -- note that this may still result in negative profits
        should there be fixed costs.
        """
        quantity = self.demand_function(price)
        # not sure this is such a good idea as it then makes the curve flat
        # which causes difficulties when solving for zeros ...
        return max(-self.cost_function(0),
                   price * quantity - self.cost_function(quantity))
    
    def monopoly_price(self):
        """
        Usual global vs. local issues ...
        """
        startSearch = 0.0
        endSearch = self.MAXPRICE
        def tmp_func(price):
            return - self.profit_function(price)
        maxPrice = optimize.fminbound(tmp_func, startSearch, endSearch)
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
    
    def monopoly_profits(self):
        return self.profit_function(self.monopoly_price())

    def marginal_cost(self, quantity):
        return derivative(self.cost_function, quantity)
    
    def competitive_price(self):
        """
        Solve c'(q(p)) = p
        
        Model situation with perfect competition where in equilibrium marginal
        profit is 0 (so marginal cost equals marginal revenue).
        
        NB: various assumptions required such as no increasing returns as well
        as that c' > 0
        """
        def tmp_func(price):
            return self.marginal_cost(self.demand_function(price)) - price
        # initialGuess should be non-zero so as to avoid problems with demand
        # functions that go to infinity there
        initialGuess = self.MAXPRICE / 2.0
        return optimize.fsolve(tmp_func, initialGuess)
    
    def monopoly_deadweight_costs(self):
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
        priceC = self.competitive_price()
        priceM = self.monopoly_price()
        quantityC = self.demand_function(priceC)
        quantityM = self.demand_function(priceM)
        totalArea = integrate.quad(self.demand_function, priceC, priceM)[0]
        return totalArea - ( (priceM - priceC) * quantityM )

    def average_cost(self, quantity):
        '''Return average cost for a given quantity of output.

        Note that if quantity = 0 will get division by zero errors. 
        To deal with this, the value at zero is approximated by value at some
        very small value epsilon.
        '''
        if quantity == 0:
            # assume continuity so this can be approximated
            eps = 0.001
            approx = self.average_cost(eps)
            return approx
        else:
            avg = self.cost_function(quantity) / quantity
            return avg

    def solve_for_zero_profits(self):
        '''Return price, quantity such that profits are zero.
        
        That is revenue exactly equal costs which is also equivalent to solving
        for average cost == price).

        Have to be a little careful since usually at least two solutions. Focus
        on the larger solution (greater than profit maximizing price).
        '''
        # want larger quantity (so smaller price)
        start = 0.0
        end = self.monopoly_price()
        # do not solve using profit_function as difficulties with numerical
        # routines due to long zero sections (e.g. when price < marginal cost)
        def tmp_func(price):
            return price - self.average_cost(self.demand_function(price)) 
        price = optimize.bisect(tmp_func, start, end)
        return price

    
class ProducerSummary(object):
    
    def __init__(self, producer, min_price = 0.0, max_price=10.0,
            min_quantity=0.0, max_quantity=10.0):
        self.p = producer
        self.min_price = min_price
        self.max_price = max_price
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity
        self.eps = self.max_price / 100.0
        self.price_values = arange(self.min_price, self.max_price, self.eps)
        self.demand_values = [ self.p.demand_function(price) for price in self.price_values ]
    
    def plot_profit_function(self):
        """
        Plot the profit function for a given producer
        """
        import pylab
        self.price_values = arange(0.0, self.max_price, self.eps)
        profitValues = [ self.p.profit_function(pp) for pp in
            self.price_values ]
        pylab.plot(self.demand_values, profitValues, color='k')
        pylab.xlabel('Price')
        pylab.ylabel('Profits')

    def info(self):
        self.competitive_price = self.p.competitive_price()
        self.monopoly_price = self.p.monopoly_price()
        self.monopoly_profits = self.p.profit_function(self.monopoly_price)
        self.competitive_output = self.p.demand_function(self.competitive_price)
        self.monopoly_output = self.p.demand_function(self.monopoly_price)
        self.dw_costs = self.p.monopoly_deadweight_costs()
        self.zero_profits_price = self.p.solve_for_zero_profits()
        self.zero_profits_output = self.p.demand_function(self.zero_profits_price)

    def print_info(self):
        self.info()
        print 'Monopoly price: ', self.monopoly_price
        print 'Monopoly demand: ', self.monopoly_output
        print 'Monopoly profits: ', self.monopoly_profits
        print 'Deadweight losses: ', self.dw_costs
        print 'Zero profits price: ', self.zero_profits_price
        print 'Zero profits demand: ', self.zero_profits_output
    
    def plot_producer_summary(self):
        """
        Plot demand function for producer with variables of interest such as
        monopoly price, competive price, deadweight loss etc.
        
        Plot in traditional manner with demand on x axis
        """
        self.info()
        import pylab
        
        self.price_values = arange(self.min_price, self.max_price, self.eps)
        self.demand_values = [ self.p.demand_function(price) for price in self.price_values ]
        # [[TODO what happens if this is infinite
        # maxDemand = min(self.p.demand_function(self.min_price), self.max_quantity)
        avg_costs = [  self.p.average_cost(dd) for dd in self.demand_values ]
        avg_costs_restricted = [ min(xx, self.max_price) for xx in avg_costs ]
        marginal_costs = [ self.p.marginal_cost(d) for d in self.demand_values ]

        fig = pylab.figure(1)
        pylab.axis(xmin=self.min_quantity, xmax=self.max_quantity,
                ymin=self.min_price, ymax=self.max_price)
        pylab.plot(self.demand_values, self.price_values, 'k')
        pylab.plot(self.demand_values, avg_costs_restricted, 'k--')
        # pylab.plot(self.demand_values, marginal_costs, 'k-.')
        pylab.xlabel('Quantity')
        pylab.ylabel('Price')
        
        newLocs = None
        newLabels = None
        def add_ticks(ticks, extraTicks):
            """
            ticks is pylab.xticks or pylab.yticks
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
        
        add_ticks(pylab.xticks, [(self.competitive_output, 'qC'), (self.monopoly_output, 'qM')])
        add_ticks(pylab.yticks, [(self.competitive_price, 'pC'), (self.monopoly_price, 'pM')])

    # TODO: these all assume demand axis origin starts at 0
    def monopoly_lines(self):
        import pylab
        pylab.axhline(self.monopoly_price, 0,
                self.monopoly_output/self.max_quantity, color='k')
        pylab.axvline(self.monopoly_output, 0,
                self.monopoly_price/self.max_price, color='k')

    def competitive_lines(self):
        import pylab
        pylab.axhline(self.competitive_price, 0,
                self.competitive_output/self.max_quantity, color='k')
        pylab.axvline(self.competitive_output, 0, self.competitive_price / self.max_quantity)

    def zero_profit_lines(self):
        import pylab
        pylab.axhline(self.zero_profits_price, 0,
                self.zero_profits_output/self.max_quantity, color='k')
        pylab.axvline(self.zero_profits_output, 0,
                self.zero_profits_price/self.max_price, color='k')

    def xrel(self, xval):
        '''Convert to relative 0-1 coordinates from absolute coordinates.'''
        return xval / (self.max_quantity - self.min_quantity)

    def yrel(self, yval):
        '''Convert to relative 0-1 coordinates from absolute coordinates.'''
        return yval / (self.max_price - self.min_price)

