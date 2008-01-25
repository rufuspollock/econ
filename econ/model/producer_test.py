import random

import econ.model.demand
import econ.model.producer

class TestProducer:
    def setup_method(self, name=''):
        self.dfConstant = 5.0
        self.dfSlope = -1.0
        self.df = econ.model.demand.get_linear_demand_function(self.dfConstant,
                                                         self.dfSlope)
        self.fixed_cost = 0.0
        self.marginalCost = 0.0
        def cost_function(quantity):
            return quantity * self.marginalCost + self.fixed_cost
        self.cf = cost_function
        self.producer = econ.model.producer.Producer(self.df, self.cf)

    def assert_almost_equal(self, x, y):
        assert round(x-y, 6) == 0

    def test_max_price_ok(self):
        exp = self.dfConstant / -self.dfSlope + 0.1 
        self.assert_almost_equal(self.producer.MAXPRICE, exp)
    
    def test_profit_function(self):
        def profit_function(price):
            return max(0,
                       self.dfConstant * price + (price ** 2) * self.dfSlope)
        maxPrice = self.producer.MAXPRICE
        numsteps = 30.0
        price = 0.0
        while price < maxPrice:
            price += maxPrice / numsteps
            self.assert_almost_equal(self.producer.profit_function(price),
                                    profit_function(price))
    
    def test_monopoly_price(self):
        self.marginalCost = 0.0
        expectedPrice = - self.dfConstant / (2 * self.dfSlope)
        assert expectedPrice == self.producer.monopoly_price()
    
    def test_monopoly_price2(self):
        self.marginalCost = 1.0
        expectedPrice = (self.dfConstant - self.dfSlope) / (-2 * self.dfSlope)
        assert expectedPrice == self.producer.monopoly_price()
    
    def test_monopoly_price_3(self):
        self.fixed_cost = 4.0
        expected = - self.dfConstant / ( 2 * self.dfSlope)
        out = self.producer.monopoly_price()
        print self.producer.profit_function(expected)
        print self.producer.profit_function(out)
        assert expected == out
    
    def test_competitive_price(self):
        """
        Constant marginal cost so very easy
        """
        self.marginalCost = 0.0
        expectedPrice = self.marginalCost
        assert expectedPrice == self.producer.competitive_price()
    
    def testGetCompetitivePrice_2(self):
        """
        Constant marginal cost so very easy
        """
        self.marginalCost = self.dfConstant * random.random()
        expectedPrice = self.marginalCost
        self.assert_almost_equal(expectedPrice, self.producer.competitive_price())
    
    def test_monopoly_deadweight_costs(self):
        self.marginalCost = self.dfConstant * random.random()
        # because linear demand function have shortcut since just a triangle
        # also use assumption of constant marginal cost)
        monopolyPrice = self.producer.monopoly_price()
        monopolyQuantity = self.producer.demand_function(monopolyPrice)
        competitiveQuantity = self.producer.demand_function(self.marginalCost)
        deadweightCosts = ( 0.5 * (monopolyPrice - self.marginalCost) * 
            ( competitiveQuantity - monopolyQuantity))
        self.assert_almost_equal(deadweightCosts,
                                self.producer.monopoly_deadweight_costs())

    def test_average_costs(self):
        self.fixed_cost = 2.0
        q1 = 0.0
        q2 = 2.0
        out1 = self.producer.average_cost(q1)
        out2 = self.producer.average_cost(q2)
        assert out1 == self.fixed_cost / 0.001
        assert out2 == 1.0

    def test_solve_for_zero_profits(self):
        self.fixed_cost = 4.0
        out = self.producer.solve_for_zero_profits()
        self.assert_almost_equal(out, 1.0)
        # max profits are 25.0 / 4
        self.fixed_cost = 25.0 /4 + 1.0
        try:
            self.producer.solve_for_zero_profits()
            assert False, 'Should raise' 
        except:
            pass
        

