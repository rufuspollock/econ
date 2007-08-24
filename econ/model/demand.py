# Convenience functions

def getLinearDemandFunction(constant, slope):
    def df(price):
        if price < 0:
            return 0
        return max(0.0, constant + slope * price)
    return df
