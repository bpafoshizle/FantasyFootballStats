from ProFootballRefDownloader import ProFootballRefDownloader

bot = ProFootballRefDownloader()

#for url in bot.getYearUrlsFromYearsPage(5):
#	print url


#for url in bot.getFantasyPlayerUrlsByYear(numPlayers=50):
#	print url

bot.downloadPlayerPagesForYear('2013')

