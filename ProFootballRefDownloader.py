import urllib2
import urlparse
import itertools
import re
#from xml.dom.minidom import parseString
from bs4 import BeautifulSoup

class ProFootballRefDownloader:
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
		self.playerGamelogUrls = None
		self.numYears = None


	def getYearPage(self):
		""" Function to get the page from PFR that contains a list of years
		for all historic NFL seasons. This function will set an internal 
		attribute that will contain the response page for further searching.
		It will also return the response page to the caller. """
		yearsUrl = self.baseUrl + "years/"
		response = urllib2.urlopen(yearsUrl)
		self.yearPage = response.read()
		return self.yearPage
	
	def getYearUrlsFromYearsPage(self, numYears=1):
		""" Function that gets a specified number of years in descending 
		order from the years page. """
		if(self.yearPage is None):
			self.getYearPage()
		
		self.numYears = numYears
		self.yearUrls = ([self.baseUrl + m.group(1) 
						 for m in 
						 itertools.islice(re.finditer(r'<a href="/(years/\d+/)">NFL</a>', self.yearPage), numYears)]
				  		)
		return self.yearUrls

	def getFantasyPlayerUrlsByYear(self, numPlayers=1):
		""" Function that will get a list of players for all
		the years specified in the yearUrls page. Default is to 
		only download the top player for each year specified. """
		if(self.yearUrls is None):
			self.getYearUrlsFromYearsPage()
			
		
		response = urllib2.urlopen(self.yearUrls[0] + "fantasy.htm")
		fantasyYearPage = response.read()
		self.playerUrls = ([self.baseUrl + m.group(1)
						   for m in
						   itertools.islice(re.finditer(r'<a href="/(players/[A-Za-z]+/\w+.htm)">\w+ \w+</a>', fantasyYearPage), 
						   numPlayers)]
						  )

		return self.playerUrls

	def getPlayerGamelogUrls(self, numYears=1, numPlayers=1):
		""" Function that will loop through the player URLs stored
		in self.playerUrls and get numYears gamelog URLs depening
		on what that player has available. Returns the list of valid 
		gamelog URLs for each player """
		
		if(self.numYears is not None):
			numYears = self.numYears

		if(self.playerUrls is None):
			self.getFantasyPlayerUrlsByYear(numPlayers=numPlayers)

		self.playerGamelogUrls = []

		for url in self.playerUrls:
			response = urllib2.urlopen(url)
			playerPage = response.read()
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
			playerGamelogPage = response.read()
			#print playerGamelogPage
			self.extractGamelogData(playerGamelogPage)


	def extractGamelogData(self, gamelogPage):
		soup = BeautifulSoup(gamelogPage)
		tableList = soup.find_all("table", id="stats", limit=1)
		print tableList
		

	

