import sys
import urllib2
import urlparse
import re


baseYahooSportsUrl = 'http://sports.yahoo.com'
yahooSportsNFLUrl = baseYahooSportsUrl + '/nfl/'


def main(argv):
	# Get Stats Page to get all the Positions
	# Drill in to every position
	
	getPlayerGameLogData()
	

def getPlayerGameLogData():
	""" Gets a table format of player game log data for
		every position available on sports.yahoo.com
	"""

	positionUrlList = getPositionUrlsFromYahooStatsPage()
	positionPages = getPositionPlayerListingPages(positionUrlList)
	playerUrls = getPlayerUrlsFromPositionPages(positionPages)


def getPlayerUrlsFromPositionPages(positionPages):
	""" Function to extract and build all the URLs for
		every player link on a position page
	"""
	playerDictList = []
	for key, value in positionPages.iteritems():
		playerPaths = re.finditer(r'<a href="(/nfl/players/\d+)">(.*?)</a>', value)
		for playerPath in playerPaths:
			playerDictList.append({'playerUrl':baseYahooSportsUrl + playerPath.group(1) + '/gamelog', 'playerName':playerPath.group(2), 'playerPos':key})
		
	
	print playerDictList




def getPositionUrlsFromYahooStatsPage():
	""" Get the initial Stats Page that will allow us to 
		bootstrap this whole process by digging in to the 
		positions pages and from there to each player and 
		game log per week per season
	"""
	yahooSportsNFLStatsUrl = yahooSportsNFLUrl + 'stats/'
	response = urllib2.urlopen(yahooSportsNFLStatsUrl)
	pageHtml = response.read()
	#statsPageFile = open('C:\Users\MILLERBARR\Documents\GitHub\FantasyFootballStats\statsPage.html', 'w')
	#statsPageFile.write(pageHtml)
	#statsPageFile.close()
	positionUrls = re.finditer(r'<a href="(/nfl/stats/byposition\?pos=.*)">.*</a>', pageHtml)
	
	return [baseYahooSportsUrl + positionUrl.group(1) for positionUrl in positionUrls]


	
def getPositionPlayerListingPages(positionUrlList):
	""" Method to create a dictionary of position pages 
		addressable by position name, e.g. QB, RB, TE, C, 
		etc, and derived from the main yahoo stats page
	"""
	positionPages = {}
	for positionUrl in positionUrlList:
		positionName = extractPositionNameFromUrl(positionUrl)
		response = urllib2.urlopen(positionUrl)
		pageHtml = response.read()
		positionPages[positionName] = pageHtml
		#positionPageFile = open('C:\Users\MILLERBARR\Documents\GitHub\FantasyFootballStats\\\\' + positionName + 'Page.html', 'w')
		#positionPageFile.write(pageHtml)
		#positionPageFile.close()

	return positionPages
	

def extractPositionNameFromUrl(positionUrl):
	"""
		Function to parse out the name of the position for a url
		using the urlparse module.
	"""
	parsedUrl = urlparse.urlparse(positionUrl)
	query = urlparse.parse_qs(parsedUrl.query)
	print query['pos']
	return query['pos'][0]
	
if __name__ == "__main__":
	main(sys.argv[1:])
