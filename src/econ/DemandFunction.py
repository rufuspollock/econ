class DemandFunction:
	
	def getDemand(self, price):
		pass

class DemandFunctionFromFunction:
	
	def __init__(self, demandFunction):
		self._demandFunction = demandFunction
	
	def getDemand(self, price):
		return self._demandFunction(price)