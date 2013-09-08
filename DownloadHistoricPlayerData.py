import sys
import urllib2
import urlparse
import re
import time
from datetime import datetime


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

	# Step 1: Get a list of all position URLs from the yahoo stats 
	# main page.
	positionUrlList = getPositionUrlsFromYahooStatsPage()
	
	# Step 2: Get a list of all pages for each URL gathered in step 1
	positionPages = getPositionPlayerListingPages(positionUrlList)

	# Step 3: Get a list of all player URLs from each position page
	# gathered in step 2.
	players = getPlayerUrlsFromPositionPages(positionPages)
	
	# Step 4: Get a list of the game log (individual game data)
	# for each year that each player has played.
	players = getAllPlayerGameLogs(players)
	#print dir(players)
	writePlayerGameLogsToFile(players)



def writePlayerGameLogToFile(playerDict):
	for url, html in playerDict['gamelogYearPages'].iteritems():
		#http://sports.yahoo.com/nfl/players/7200/gamelog?year=2012	
		print url
		year = re.findall(r'year=(\d\d\d\d)', url)[0]
		#print year
		playerPos = playerDict['playerPos']
		playerName = playerDict['playerName']
		fileName = '%s_%s_%s.html' % (playerPos, playerName, year)
	
		outFile = open('playerGamelogs/%s' % fileName, 'w')
		outFile.write(html)
		outFile.close()
						

def getAllPlayerGameLogs(players):
	""" Function to take a list of all player
		dictionaries and loop through them getting the year
	"""
	# put a list comprehension here to 
	for playerDict in [player for player in players if not(havePlayer(player))]:
		playerDict = getPlayerYears(playerDict)
		playerDict = addPlayerYearGamelogPages(playerDict)
		writePlayerGameLogToFile(playerDict)
		logHavePlayer(playerDict)


	return players


def havePlayer(player):
	""" Check the player against our database to see if 
	 	we have this player yet
	"""
	player['playerName']

def logHavePlayer(playerDict):
	""" Function will log an update to the sqlLite db
		indicating that we have downloaded all the logs
		for a given player.
	"""

def getPlayerYears(playerDict):
	""" Function to extract all the relevant years
		that a player played based on what is in their 
		base gamelog page. Returns a list of year Urls with the player dict
	"""
	currentYear = str(datetime.now().year-1)
	print "Opening %s" % playerDict['playerUrl']
	response = urllib2.urlopen(playerDict['playerUrl'])
	pageHtml = response.read()
	response.close()
	#playerBaseGameLog = open('/Users/bpafoshizle/github/local/FantasyFootballStats/%s.html' % playerDict['playerName'], 'w')
	#playerBaseGameLog.write(pageHtml)
	yearLinks = re.finditer(r'<a href="(/nfl/players/\d+/gamelog\?year=\d\d\d\d)">\d\d\d\d</a>', pageHtml)
	playerDict['gameLogYearUrls'] = ['%s?year=%s' % (playerDict['playerUrl'], currentYear)]
	for yearLink in yearLinks:
		#print yearLink.group(1)
		playerDict['gameLogYearUrls'].append('%s%s' % (baseYahooSportsUrl, yearLink.group(1)))
		
	print playerDict['gameLogYearUrls']

	# Sleep for 3 seconds after each request
	time.sleep(3)
	return playerDict

	
def addPlayerYearGamelogPages(playerDict):
	""" Function to loop through and grab the HTML for
		each year page of gamelogs for the passed-in 
		year list. Add this HTML in a page list or dict data 
		structure.
	"""
	playerDict['gamelogYearPages'] = {}
	for gameLogYearUrl in playerDict['gameLogYearUrls']:
		response = urllib2.urlopen(gameLogYearUrl)
		playerDict['gamelogYearPages'][gameLogYearUrl] = response.read()
		response.close()
		time.sleep(3)

	return playerDict

def getPlayerUrlsFromPositionPages(positionPages):
	""" Function to extract and build all the URLs for
		every player link on a position page
	"""
	playerDictList = []
	for key, value in positionPages.iteritems():
		playerPaths = re.finditer(r'<a href="(/nfl/players/\d+)">(.*?)</a>', value)
		for playerPath in playerPaths:
			playerDictList.append({'playerUrl':baseYahooSportsUrl + playerPath.group(1) + '/gamelog', 'playerName':playerPath.group(2), 'playerPos':key})
			logPlayer(playerPath.group(1), playerPath.group(2), key) # log to sqlLite
			break
		break
		
	
	return playerDictList


def logPlayer(playerId, playerName, position):
	""" Method to initially add a player in to our SqlLite database
		We will add the player if we don't already have it
	"""
	

def getPositionUrlsFromYahooStatsPage():
	""" Get the initial Stats Page that will allow us to 
		bootstrap this whole process by digging in to the 
		positions pages and from there to each player and 
		game log per week per season
	"""
	yahooSportsNFLStatsUrl = yahooSportsNFLUrl + 'stats/'
	response = urllib2.urlopen(yahooSportsNFLStatsUrl)
	pageHtml = response.read()
	response.close()
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
		response.close()
		positionPages[positionName] = pageHtml
		#positionPageFile = open('C:\Users\MILLERBARR\Documents\GitHub\FantasyFootballStats\\\\' + positionName + 'Page.html', 'w')
		#positionPageFile.write(pageHtml)
		#positionPageFile.close()
		break

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
