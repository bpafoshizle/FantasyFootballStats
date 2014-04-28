import sys
from WebBot.ProFootballRefBot import ProFootballRefBot
from Extractor.ProFootballRefExtractor import ProFootballRefExtractor


def main(argv):
	#bot = ProFootballRefBot()
	#bot.downloadGamelogPagesForYear('2013')
	extractor = ProFootballRefExtractor(sourceDataDir='./Data/Raw/ProFootballRef/Testing')
	extractor.extractPlayerGameLogData()

	
if(__name__ == '__main__'):
	main(sys.argv[1:])
