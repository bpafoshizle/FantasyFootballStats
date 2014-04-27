import sys
from WebBot.ProFootballRefBot import ProFootballRefBot


def main(argv):
	bot = ProFootballRefBot()
	bot.downloadGamelogPagesForYear('2013')

	
if(__name__ == '__main__'):
	main(sys.argv[1:])