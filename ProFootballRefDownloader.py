import urllib2
import urlparse
import itertools
import re


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
			print self.yearUrls
			
		
		response = urllib2.urlopen(self.yearUrls[0] + "fantasy.htm")
		fantasyYearPage = response.read()
		self.playerUrls = ([self.baseUrl + m.group(1)
						   for m in
						   								 #<a href="/players/C/CousKi00.htm">Kirk Cousins</a>
						   itertools.islice(re.finditer(r'<a href="/(players/[A-Za-z]+/\w+.htm)">\w+ \w+</a>', fantasyYearPage), 
						   numPlayers)]
						  )

		return self.playerUrls
