from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join, splitext, basename
from bpaUtils import BpaUtils
import csv
import re

class PlayerPage:
	""" Class to help with the management of player pages and the
	differences in positions """

	def __init__(self, name, position):
		self.position = position
		self.name = name
		self.statsTabs = {}
		self.stats = {}


class ProFootballRefExtractor:
	""" Class to extract data from HTML files downloaded from 
	http://www.pro-football-reference.com/ and output data to 
	CSV files, which can be used as clean data sources to load 
	a database. """

	def __init__(self, sourceDataDir='./Data/Raw/ProFootballRef/',
				destDataDir='./Data/CSV/ProFootballRef/'):
		self.sourceDataDir = sourceDataDir
		self.destDataDir = destDataDir
		self.sourceGameLogDir = join(sourceDataDir, 'playerGameLogPages')
		self.sourcePlayerDir = join(sourceDataDir, 'playerPages')
		self.utils = BpaUtils()
		
	def extractPlayerData(self):
		""" Method that will extract player data from player pages"""
		htmlFiles = self.getHtmlFiles(self.sourcePlayerDir)
		for htmlFile in htmlFiles:
			soup = BeautifulSoup(open(htmlFile))
			playerName = splitext(basename(htmlFile))[0]
			position = self.getPosition(soup)

			playerPage = PlayerPage(playerName, position)

			# Get stat tables from the html
			playerPage = self.getPlayerPageStats(soup, playerPage)

			
			for statsType, statsTab in playerPage.statsTabs.items():	
				# Get the format of the regular season and playoff tables 
				if(statsType == 'Pass'):
					tabForm = self.getTabFormat(statsTab, statsType)
				else:
					tabForm = self.getTabFormat(statsTab)

				# transform the column header data into python lists
				header = self.utils.bsThResultSetToList(tabForm)
				
				# Get just the rows from the table that have meaningful data,
				cleanStats = self.extractStatsRows(statsTab)

				# turn the cleaned up data stats rows into a friendlier python list of lists
				statsList = self.utils.bsTrResultSetToList(cleanStats)
				
				# affix header to data
				statsList.insert(0, header)

				playerPage.stats[statsType] = statsList

				fileName = join(self.destDataDir, playerPage.name) + "_" + playerPage.position + "_" + statsType
				print("Writing " + fileName)
				self.writeListToFile(fileName, statsList)
	
	def extractPlayerGameLogData(self):
		""" Method to extract game log data from player game log pages""" 
		htmlFiles = self.getHtmlFiles(self.sourceGameLogDir)
		for htmlFile in htmlFiles:
			playerName = splitext(basename(htmlFile))[0]
			soup = BeautifulSoup(open(htmlFile))
			
			# Get both the regular season and playoff tables from the html
			regSeasStatsTab, poStatsTab = self.getGamelogStatsTables(soup)	
			
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

			#print(regSeasStatList)
			#print(poStatsForm)
			#print(poStatList)
			self.writeListToFile(
				join(self.destDataDir, playerName) + '_reg', 
				regSeasStatList
			)

			self.writeListToFile(
				join(self.destDataDir, playerName) + '_po', 
				poStatList
			)


	def writeListToFile(self, name, plist):
		""" Method to take some python list and write it to a file for
		viewing or incorporation to another program"""
		with open(name + ".txt", "w") as f:
			writer = csv.writer(f)
			writer.writerows(plist)

	def writeSoupToFile(self, name, soup):
		""" Method to take some HTML block and write it to a file for 
		easier viewing """
		f = open(name + ".txt", "w")
		f.write(u'\n'.join(map(str, soup)))
		f.close()
		
		
	
	def extractStatsRows(self, soup):
		""" Method to extract all the stats rows from a valid
		table from the PFR website by excluding header rows
		embedded within the tables separating years"""
		return soup.tbody.find_all(self.trNoThreadAttr)


	def getTableById(self, soup, id):
		return soup.find('table', id=id)

	def getPlayerPageStats(self, soup, playerPage):
		position = playerPage.position
		if(position == "QB"):
			return self.getPassAndRushStats(soup, playerPage)
		elif(position == "RB"):
			return self.getRushAndRecStats(soup, playerPage)
		elif(position in ["WR", "TE"]):
			return self.getRecAndRushStats(soup, playerPage)

	def getPosition(self, soup):
		#print(soup.find_all("Stronger", text="Position"))
		divs = soup.find_all("div", class_="float_left")

		for snippet in divs:
			m = re.search("Position:</strong> (\w\w).*", str(snippet))
			if(m):
				return m.group(1)


	def getRushAndRecStats(self, soup, playerPage):
		playerPage.statsTabs['RushAndRec'] = self.getTableById(soup, 'rushing_and_receiving')
		return playerPage

	def getRecAndRushStats(self, soup, playerPage):
		playerPage.statsTabs['RecAndRush'] = self.getTableById(soup, 'receiving_and_rushing')
		return playerPage

	def getPassAndRushStats(self, soup, playerPage):
		playerPage.statsTabs['Pass'] = self.getTableById(soup, 'passing')
		playerPage.statsTabs['RushAndRec'] = self.getTableById(soup, 'rushing_and_receiving')
		return playerPage
	
	def getGamelogStatsTables(self, soup):
		regSeasStatsTab = self.getTableById(soup, 'stats')#soup.find('table', id='stats')
		poStatsTab = self.getTableById(soup, 'stats_playoffs')#soup.find('table', id='stats_playoffs')
		return regSeasStatsTab, poStatsTab

	def getTabFormat(self, tab, tabType=None):	
		statHeaders = tab.thead.find_all(self.dataStatNonBlankNoHeader)
		
		if(tabType is None):
			statOverHeaders = tab.thead.find_all("tr", "over_header")[0].find_all("th")
			fullyQualifiedHeader = self.combineOverHeaderWithHeader(statOverHeaders, statHeaders)
		else:
			fullyQualifiedHeader = self.combineTabTypeWithHeader(tabType, statHeaders)
		return fullyQualifiedHeader

	def combineTabTypeWithHeader(self, tabType, statHeaders):
		for statHeader in statHeaders:
			statHeader.string = tabType + '_' + statHeader.string
		
		return statHeaders

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
		
	def getHtmlFiles(self, source):
		return [join(source, f) 
				for f in listdir(source) 
				if isfile(join(source, f))
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
