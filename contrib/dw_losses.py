import econ.data.plot

import econ.model.producer as p
import econ.model.demand as d


def example():
    dfConstant = 9.0
    dfSlope = -1.0
    df = d.getLinearDemandFunction(dfConstant, dfSlope)
    marginalCost = 1.0
    fixedCost = 9.0
    def costs(quantity):
        if quantity <= 0:
            return 0
        else:
            return quantity * marginalCost + fixedCost
    producer = p.Producer(df, costs)
    summary = p.ProducerSummary(producer)
    # summary.plotProfitFunction()
    summary.plotProducerSummary()

if __name__ == '__main__':
    example()
    import matplotlib
    matplotlib.use('PS')
    import pylab
    pylab.savefig('tmp.png')
