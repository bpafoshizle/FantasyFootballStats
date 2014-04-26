
class BpaUtils:
	""" A class to hold utility methods and constructs for 
	bpa's coding benefits """

	def __init__(self):
		self.Name = 'bpaUtils'

	def writeStringToTempFile(self, fileName, string):
		with open('./tempFiles/' + fileName, 'w') as f:
			f.write(string)

