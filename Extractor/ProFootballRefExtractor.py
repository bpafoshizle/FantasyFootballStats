from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from bpaUtils import BpaUtils

class ProFootballRefExtractor:
	""" Class to extract data from HTML files downloaded from 
	http://www.pro-football-reference.com/ and output data to 
	CSV files, which can be used as clean data sources to load 
	a database. """

	def __init__(self, sourceDataDir='./Data/Raw/ProFootballRef/'):
		self.sourceDataDir = sourceDataDir
		self.sourceGameLogDir = join(sourceDataDir, 'playerGameLogPages')
		self.sourcePlayerDir = join(sourceDataDir, 'playerPages')
		self.utils = BpaUtils()
		
	def extractPlayerData(self):
		""" Method that will extract player data from player pages"""
		
	
	def extractPlayerGameLogData(self):
		""" Method to extract game log data from player game log pages""" 
		htmlFiles = self.getHtmlFiles()
		for htmlFile in htmlFiles:
			soup = BeautifulSoup(open(htmlFile))
			
			# Get both the regular season and playoff tables from the html
			regSeasStatsTab, poStatsTab = self.getStatsTables(soup)	
			
			# Get the format of the regular season and playoff tables 
			regSeasStatsForm = self.getTabFormat(regSeasStatsTab)
			poStatsForm = self.getTabFormat(poStatsTab)
			
			# transform the column header data into python lists
			regSeasStatsHeader = self.utils.bsThResultSetToList(regSeasStatsForm)
			poStatsHeader = self.utils.bsThResultSetToList(poStatsForm)
			
			# Get just the rows from the table that have meaningful data,
			# discarding embedded extra headers
			regSeasonCleanStats = self.extractStatsRows(regSeasStatsTab)
			poCleanStats = self.extractStatsRows(poStatsTab)
			
			# turn the cleaned up data stats rows into a friendlier python list of lists
			regSeasStatList = self.utils.bsTrResultSetToList(regSeasonCleanStats)
			poStatList = self.utils.bsTrResultSetToList(poCleanStats)

			# affix header to data
			regSeasStatList.insert(0, regSeasStatsHeader)
			poStatList.insert(0, poStatsHeader)

			print(regSeasStatList)
			#print(poStatsForm)
			print(poStatList)


	def writeSoupToFile(self, name, soup):
		""" Method to take some HTML block and write it to a file for 
		easier viewing """
		f = open(name + ".txt", "w")
		f.write(u'\n'.join(map(str, soup)))
		
		
	
	def extractStatsRows(self, soup):
		""" Method to extract all the stats rows from a valid
		table from the PFR website by excluding header rows
		embedded within the tables separating years"""
		return soup.tbody.find_all(self.trNoThreadAttr)


	def getStatsTables(self, soup):
		regSeasStatsTab = soup.find('table', id='stats')
		poStatsTab = soup.find('table', id='stats_playoffs')
		return regSeasStatsTab, poStatsTab

	def getTabFormat(self, tab):
		statOverHeaders = tab.thead.find_all("tr", "over_header")[0].find_all("th")
		statHeaders = tab.thead.find_all(self.dataStatNonBlankNoHeader)

		fullyQualifiedHeader = self.combineOverHeaderWithHeader(statOverHeaders, statHeaders)

		return fullyQualifiedHeader
	
	def combineOverHeaderWithHeader(self, oh, h):
		""" Method to look over each header column, and
		augment the name of the column with the appropriate 
		header column for as many columns as necessary. This
		is necessary to qualify rec yards from rushing yards
		for example, where the column name is exactly the same.
		"""
		# Step 1: Set counter to first header column.
		hCntr = 0
		ohCntr = 0


		while(hCntr < len(h) and ohCntr < len(oh)):
			# Step 2: Get first overheader column. If it has a colspan, then
			#	loop over that many header columns and concatenate the OH name 
			#	with each H name.
			ohTh = oh[ohCntr]
			ohColSpan = ohTh.get("colspan", 1)
			ohText = ohTh.get_text()
			
			# Concatenate oh text with header text
			for i in range(int(ohColSpan)):
				hTh = h[hCntr]
				hText = hTh.get_text()
				
				if(ohText != ""):
					# Step 3: update header column counter and repeat process.
					hTh.string = ohText + "_" + hText
				#print(hTh.get_text())
				hCntr = hCntr + 1
				

			# Increment to grab next Overheader column
			ohCntr = ohCntr + 1

		#print(oh)
		#print(h)
		return h
		
	def getHtmlFiles(self):
		return [join(self.sourceGameLogDir, f) 
				for f in listdir(self.sourceGameLogDir) 
				if isfile(join(self.sourceGameLogDir, f))
				and not f.startswith('.')]

				
	# Soup find_all mapping methods
	def trNoThreadAttr(self, tag):
		""" Method that returns true if a tag is a tr type and
		contains an id attribute"""
		return (tag.name == 'tr') and (tag.has_attr('id'))
		
	def dataStatNonBlankNoHeader(self, tag):
		"""Method to return true when a tag is a "th", when 
		it has a data-stat value that is not empty and doesn't 
		contain the word "Header" """
		if(tag.name == "th"):
			if(tag.has_attr("data-stat")):
				ds = tag["data-stat"]
				if(ds != ""):
					if("header" not in ds):
						return True
		return False
