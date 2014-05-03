from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join


class ProFootballRefExtractor:
	""" Class to extract data from HTML files downloaded from 
	http://www.pro-football-reference.com/ and output data to 
	CSV files, which can be used as clean data sources to load 
	a database. """

	def __init__(self, sourceDataDir='./Data/Raw/ProFootballRef/'):
		self.sourceDataDir = sourceDataDir
		self.sourceGameLogDir = join(sourceDataDir, 'playerGameLogPages')
		self.sourcePlayerDir = join(sourceDataDir, 'playerPages')
		
	def extractPlayerData(self):
		""" Method that will extract player data from player pages"""
		
	
	def extractPlayerGameLogData(self):
		""" Method to extract game log data from player game log pages""" 
		htmlFiles = self.getHtmlFiles()
		for htmlFile in htmlFiles:
			soup = BeautifulSoup(open(htmlFile))
			regSeasStatsTab, poStatsTab = self.getStatsTables(soup)	
			regSeasStatsForm = self.getTabFormat(regSeasStatsTab)
			poStatsForm = self.getTabFormat(poStatsTab)
			
			regSeasonCleanStats = self.extractStatsRows(regSeasStatsTab)
			poCleanStats = self.extractStatsRows(poStatsTab)
			#print(regSeasStatsForm)
			#print(regSeasonCleanStats)
			#print(poStatsForm)
			print(poCleanStats)

	
	def extractStatsRows(self, soup):
		""" Method to extract all the stats rows from a valid
		table from the PFR website by excluding header rows
		embedded within the tables separating years"""
		return soup.tbody.find_all(self.trNoThreadAttr)

	def trNoThreadAttr(self, tag):
		""" Method that returns true if a tag is a tr type and
		contains an id attribute"""
		return (tag.name == 'tr') and (tag.has_attr('id'))

	def getStatsTables(self, soup):
		regSeasStatsTab = soup.find('table', id='stats')
		poStatsTab = soup.find('table', id='stats_playoffs')
		return regSeasStatsTab, poStatsTab

	def getTabFormat(self, tab):
		return tab.thead.find_all('th', attrs={'data-stat': True})

	def getHtmlFiles(self):
		return [join(self.sourceGameLogDir, f) 
				for f in listdir(self.sourceGameLogDir) 
				if isfile(join(self.sourceGameLogDir, f))
				and not f.startswith('.')]
