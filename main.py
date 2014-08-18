import sys
from WebBot.ProFootballRefBot import ProFootballRefBot
from Extractor.ProFootballRefExtractor import ProFootballRefExtractor


def main(argv):
	#bot = ProFootballRefBot()
	#bot.downloadGamelogPagesForYear('2013')
	
	#### Tested 2014-08-17 works fine. Writes to files ####
	#extractor = ProFootballRefExtractor(sourceDataDir='./Data/Raw/ProFootballRef/Testing')
	#extractor.extractPlayerGameLogData()

	extractor = ProFootballRefExtractor(sourceDataDir = './Data/Raw/ProFootballRef/Testing')
	extractor.extractPlayerData()

	
if(__name__ == '__main__'):
	main(sys.argv[1:])
