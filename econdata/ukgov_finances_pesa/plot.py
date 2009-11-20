import data

import pylab
class Plots(object):
    def __init__(self):
        self.a = data.Analyzer()

    def crude_totals(self):
        entries, years = self.a.extract_simple()
        expenditure = entries['Public sector current expenditure']
        pylab.plot(years, expenditure)
        pylab.xlim(xmin=2000)
        pylab.savefig('expenditure.png')

    def dept_spend(self):
        out = self.a.extract_dept_spend()
        # delete very small items 
        for k in out.keys():
            if out[k] < 2000: # anything less than 2 billion
                del out[k]
        labels = out.keys()
        # labels = [ l.replace(' ', '\n') for l in labels ]
        pylab.figure(figsize=(12,12))
        pylab.pie(out.values(), labels=labels, labeldistance=1.3)
        pylab.savefig('dept_expenditure.png')

if __name__ == '__main__':
    p = Plots()
    p.crude_totals()
    p.dept_spend()

