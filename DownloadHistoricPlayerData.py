import sys
import urllib2
import urlparse
import re


baseYahooSportsUrl = 'http://sports.yahoo.com'
yahooSportsNFLUrl = baseYahooSportsUrl + '/nfl/'



def main(argv):
	# Get Stats Page to get all the Positions
	# Drill in to every position
	
	getPositionPlayerListingPage()
	
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


	
def getPositionPlayerListingPages():
	for positionUrl in getPositionUrlsFromYahooStatsPage():
		positionName = extractPositionNameFromUrl(positionUrl)
		response = urllib2.urlopen(positionUrl)
		pageHtml = response.read()
		positionPageFile = open('C:\Users\MILLERBARR\Documents\GitHub\FantasyFootballStats\\\\' + positionName + 'Page.html', 'w')
		positionPageFile.write(pageHtml)
		positionPageFile.close()
	

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