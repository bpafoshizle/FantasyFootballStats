from bs4 import BeautifulSoup

class BpaUtils:
	""" A class to hold utility methods and constructs for 
	bpa's coding benefits """

	def __init__(self):
		self.Name = 'bpaUtils'

	def writeStringToTempFile(self, fileName, string):
		with open('./tempFiles/' + fileName, 'w') as f:
			f.write(string)

	def htmlTabToList(self, table):
		""" Method that will take an extracted and cleaned html table 
        and make a list (rows) of lists (columns)
        """ 
		result = []
		allrows = table.findAll('tr')
		for row in allrows:
			result.append([])
			allcols = row.findAll('td')
			for col in allcols:
				thestrings = [str(s) for s in col.findAll(text=True)]
				thetext = ''.join(thestrings)
				result[-1].append(thetext)
		return result


	def bsResultSetToList(self, resultSet):
		""" Method to take a result set of table rows (tr)
		from BeautifulSoup's findAll and turn them into a list of data.
		"""
		result = []
		for tr in resultSet:
			result.append([])
			result[-1].append([self.parse_string(e) for e in tr.findAll('td')])
		return result




	# Helper function to return concatenation of all character data in an element
	def parse_string(self, el):
		text = ''.join([str(s) for s in el.findAll(text=True)])
		return text.strip()
