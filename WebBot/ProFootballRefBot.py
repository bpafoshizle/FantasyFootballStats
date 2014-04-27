try:
	import urllib.request as urllib2
except:
	import urllib2
try:
	import urllib.parse as urlparse
except:
	import urlparse
	

import itertools
import re	
from bs4 import BeautifulSoup
from bpaUtils import BpaUtils

class ProFootballRefBot:
	""" Class the represents a bot to manipulate the 
	http://www.pro-football-reference.com/ website, which
	contains a plethora of detail NFL data and interesting 
	statistics, and which will be referred to in further comments
	as PFR as a shorthand"""

	def __init__(self):
		""" Initialize the downloader object """
		self.baseUrl = "http://www.pro-football-reference.com/"
		self.yearPage = None
		self.yearUrls = None
		self.playerUrls = None
		#self.playerGamelogUrls = None
		self.numYears = None
		self.bpaUtils = BpaUtils()


	def getYearPage(self):
		""" Function to get the page from PFR that contains a list of years
		for all historic NFL seasons. This function will set an internal 
		attribute that will contain the response page for further searching.
		It will also return the response page to the caller. """
		yearsUrl = self.baseUrl + "years/"
		response = urllib2.urlopen(yearsUrl)
		self.yearPage = response.read().decode('utf-8')
		return self.yearPage
	
	def getYearUrlsFromYearsPage(self, numYears=1):
		""" Function that gets a specified number of years in descending 
		order from the years page. Calls getYearPage(), if it hasn't 
		already been called."""
		if(self.yearPage is None):
			self.getYearPage()
		
		self.numYears = numYears
		self.yearUrls = ([self.baseUrl + m.group(1) 
						 for m in 
						 itertools.islice(re.finditer(r'<a href="/(years/\d+/)">NFL</a>', self.yearPage), numYears)]
						)
		return self.yearUrls

	def getFantasyPlayerUrlsByYear(self, year, numPlayers=1):
		""" Function that will get a list of players for all
		the years specified in the yearUrls page. Default is to 
		only download the top player for each year specified. 
		Calls getYearUrlsFromYearsPage(), if it hasn't already been
		called."""
		if(self.yearUrls is None):
			self.getYearUrlsFromYearsPage()
			
		yearUrl = [u for u in self.yearUrls if year in u][0]
		response = urllib2.urlopen(yearUrl + "fantasy.htm")
		fantasyYearPage = response.read().decode('utf-8')
		self.playerUrls = ([self.baseUrl + m.group(1)
						   for m in
														 #<a href="/players/C/CousKi00.htm">Kirk Cousins</a>
						   itertools.islice(re.finditer(r'<a href="/(players/[A-Za-z]+/\w+.htm)">\w+ \w+</a>', fantasyYearPage), 
						   numPlayers)]
						  )

		return self.playerUrls
	
	def downloadPlayerPagesForYear(self, year):
		"""Method to download players for a year
		passed as a parameter. Calls getFantasyPlayerUrlsByYear(),
		if it hasn't already been called."""
		if(self.playerUrls is None):
			self.getFantasyPlayerUrlsByYear(year, numPlayers=1000)

		for playerUrl in self.playerUrls:
			response = urllib2.urlopen(playerUrl)
			playerPage = response.read().decode('utf-8')
			playerName = self.extractPlayerNameFromPlayerPage(playerPage)
			filePath = './Data/Raw/ProFootballRef/playerPages/' + playerName + '_' + year + '.html'
			print('Writing: %s' % filePath)
			#self.bpaUtils.writeStringToTempFile('playerPage.html', playerPage)
	
	def downloadGamelogPagesForYear(self, year):
		"""Method to download players gamelog pages
		to get detailed data about each game a player 
		has participated in. Calls getFantasyPlayerUrlsByYear(),
		if it hasn't already been called."""
		if(self.playerUrls is None):
			self.getFantasyPlayerUrlsByYear(year, numPlayers=1000)
			
		for playerUrl in self.playerUrls:
				gameLogUrl = self.makeGameLogUrl(playerUrl)
				print('Downloading: %s' % gameLogUrl)
				response = urllib2.urlopen(gameLogUrl)
				playerGamelogPage = response.read().decode('utf-8')
				playerName = self.extractPlayerNameFromGameLogPage(playerGamelogPage)
				filePath = './Data/Raw/ProFootballRef/playerGameLogPages/' + playerName + '_GameLog.html'
				print('Writing: %s' % filePath)
				with open(filePath, 'w') as f:
					f.write(playerGamelogPage)
	
	def makeGameLogUrl(self, playerUrl):
		"""use http://www.pro-football-reference.com/players/F/FavrBr00.htm
		to produce http://www.pro-football-reference.com/players/F/FavrBr00/gamelog//"""
		return re.sub(r'\.htm', r'/gamelog//', playerUrl)
	
	def extractPlayerNameFromPlayerPage(self, playerPage):
		"""Method to extract a player's name from the player page html
		passed as a parameter."""
		#<meta itemprop="name" content="Drew Brees">
		#<meta itemprop="name" content="Jamaal Charles">
		#print playerPage
		pattern = re.compile(r'<meta itemprop="name" content="(.*)">')
		result = pattern.search(playerPage)
		return result.group(1)
		
	def extractPlayerNameFromGameLogPage(self, playerGamelogPage):
		"""Method to extract a player's name from the player page html
		passed as a parameter."""
		#<h1 class="float_left" style="vertical-align: middle;">Jamaal Charles</h1>
		#self.bpaUtils.writeStringToTempFile('playerGamelogPage.html', playerGamelogPage)
		pattern = re.compile(r'<h1 class="float_left" style="vertical-align: middle;">(.*)</h1>')
		result = pattern.search(playerGamelogPage)
		print(result.group(1))
		return result.group(1)

	def extractGamelogData(self, gamelogPage):
		soup = BeautifulSoup(gamelogPage)
		tableList = soup.find_all("table", id="stats", limit=1)
		print(tableList)

###################################### DEPRECATED ######################################

	def getPlayerGamelogUrls(self, numYears=1, numPlayers=1):
		""" Function that will loop through the player URLs stored
		in self.playerUrls and get numYears gamelog URLs depening
		on what that player has available. Returns the list of valid 
		gamelog URLs for each player.  This function may not be as useful
		since you can just use http://www.pro-football-reference.com/players/F/FavrBr00.htm
		to produce http://www.pro-football-reference.com/players/F/FavrBr00/gamelog//"""
		
		if(self.numYears is not None):
			numYears = self.numYears

		if(self.playerUrls is None):
			self.getFantasyPlayerUrlsByYear(numPlayers=numPlayers)

		self.playerGamelogUrls = []

		for url in self.playerUrls:
			response = urllib2.urlopen(url)
			playerPage = response.read().decode('utf-8')
			self.playerGamelogUrls.extend (
										   self.sortGamelogList(
										   	[
												(self.baseUrl + m.group(1), m.group(2))
									  			for m in
									  				re.finditer(r'<a href="/(players/[A-Za-z]+/\w+/gamelog/\d\d\d\d/)">(\d\d\d\d)</a>', playerPage)
									  	   	]
										   )[0:numYears]
									 	  )
		return self.playerGamelogUrls
	
	
	def sortGamelogList(self, gamelogList, Descending=True):
		"""Function that takes a list of lists. The inner list
		consists of one gamelog URL plus the year to facilitate sorting.
		Returns a list of just the URLs sorted desc"""

		# Sort the list, but convert from set back to list first as a cool hack to remove duplicates
		return sorted(list(set(gamelogList)), key=lambda gamelogTuple : gamelogTuple[1], reverse=Descending) # sort by the second element: year	
		
	def getPlayerPagesAndExtractStats(self, playerGamelogUrlYearTuples):
		for urlYearTuple in playerGamelogUrlYearTuples:
			#print urlYearTuple[0]
			response = urllib2.urlopen(urlYearTuple[0])
			playerGamelogPage = response.read().decode('utf-8')
			#print playerGamelogPage
			self.extractGamelogData(playerGamelogPage)

	

