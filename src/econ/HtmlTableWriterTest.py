import unittest

from HtmlTableWriter import HtmlTableWriter

class HtmlTableWriterTest(unittest.TestCase):
	"""
	[[TODO: replace test-by-eye with something decent
	"""
	def testSimple(self):
		indata1 = [[1,1], [0,1]]
		expected = '<table class="data"><tbody><tr><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td></tr></tbody></table>'
		writer1 = HtmlTableWriter()
		writer1.doPrettyPrint = False
		
		out1 = writer1.writeTable(indata1)
		self.assertEquals(expected, out1)
	
	def testColHeadings(self):
		indata1 = [[1,1], [0,1]]
		headings = ['x','y']
		caption = ''
		expected = '<table class="data"><thead><tr><th>x</th><th>y</th></tr></thead><tbody><tr><td>1</td><td>1</td></tr><tr><td>0</td><td>1</td></tr></tbody></table>'
		writer1 = HtmlTableWriter()
		writer1.doPrettyPrint = False
		
		# no caption but headings
		out1 = writer1.writeTable(indata1, caption, headings)
		self.assertEquals(expected, out1)
	
	def testRowHeadings(self):
		indata1 = [[1,1], [0,1]]
		headings = ['x','y']
		rowHeadings = ['Date 1', 'Date 2']
		caption = ''
		expected = '<table class="data"><thead><tr><th></th><th>x</th><th>y</th></tr></thead><tbody><tr><th>Date 1</th><td>1</td><td>1</td></tr><tr><th>Date 2</th><td>0</td><td>1</td></tr></tbody></table>'
		writer1 = HtmlTableWriter()
		writer1.doPrettyPrint = False
		
		# no caption but headings
		out1 = writer1.writeTable(indata1, caption, headings, rowHeadings)
		self.assertEquals(expected, out1)
		
		
	
	def testPrettyPrint(self):
		in1 = '<table><tr><th>x</th><th>y</th></tr><tr><td>0</td><td>1</td></tr></table>'
		writer1 = HtmlTableWriter()
		# print writer1.prettyPrint(in1)