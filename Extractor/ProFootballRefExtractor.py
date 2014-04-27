from bs4 import BeautifulSoup


class ProFootballRefExtractor:
	""" Class to extract data from HTML files downloaded from 
	http://www.pro-football-reference.com/ and output data to 
	CSV files, which can be used as clean data sources to load 
	a database. """

	def __init__(self, dataDir='./Data/Raw/ProFootballRef/'):
		self.dataDir = dataDir
		
	def extractPlayerData(self):
		""" Method that will extract player data from player pages"""
		
	
	def extractPlayerGameLogData(self):
		""" Method to extract game log data from player game log pages""" 