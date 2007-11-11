import econ.mdg 

class TestDownloadData:

    def test_1(self):
        # series 580: Population below $1 (PPP) per day consumption,
        # percentage
        out = econ.mdg.download_data(580)
        assert len(out) > 0
        print out[:30]


class TestMdgMetadata:

    def setup_class(self):
        self.meta = econ.mdg.MdgMetadata()
        self.series = self.meta.series

    def test_series(self):
        assert len(self.series) == 126

    def test_series_2(self):
        title = 'Agriculture support estimate for OECD countries as percentage of their GDP'
        assert self.series[654] == title


