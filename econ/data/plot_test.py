from econ.data.plot import Series
import econ.data.plot

class TestSeries:

    xvals = [1,2,3]
    yvals = [x**2 for x in xvals]
    series1 = Series(xvals, yvals)


class TestTabularToSeries:
    data = [
            [ '1', '2', '3' ],
            [ '5', '6', '7' ],
        ]

    def test_1(self):
        # series = econ.data.plot.table_to_series(data)
        # assert len(series) == 2
        pass

    def test_parse_column(self):
        incols = [
                [ 'Header', '1', '2', '3' ],
                [ '1', '-', '2', '3' ],
                ]
        expcols = [
                ( [ 1, 2, 3 ], [], [] ),
                ( [ 1, 2, 3 ], [1], [] ),
                ]
        for ii in range(len(incols)):
            out, skipped, probs = econ.data.plot.parse_column(incols[ii])
            assert out == expcols[ii][0]
            assert skipped == expcols[ii][1]
            assert probs == expcols[ii][2]


class TestPloticus:

    plotter = econ.data.plot.Ploticus()
    xdata  = [ 1, 2, 3 ]
    ydata = [ 4, 5, 6 ]


    def test__make_csv(self):
        out = self.plotter._make_csv(self.xdata, self.ydata)
        assert out.startswith('1, 4\n')
   
    def test_line(self):
        out = self.plotter.line(self.xdata, self.ydata)
        assert len(out) > 0, out

    def test_pie(self):
        out = self.plotter.pie(self.xdata, self.ydata)
        assert len(out) > 0

    def test_pie(self):
        out = self.plotter.vbar(self.xdata, self.ydata)
        assert len(out) > 0

