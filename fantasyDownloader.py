from ProFootballRefDownloader import ProFootballRefDownloader

bot = ProFootballRefDownloader()

#for url in bot.getYearUrlsFromYearsPage(5):
#	print url


#for url in bot.getFantasyPlayerUrlsByYear(numPlayers=50):
#	print url

<<<<<<< HEAD
bot.downloadPlayerPagesForYear('2013')

=======
playerUrls = bot.getPlayerGamelogUrls(numYears=2,numPlayers=1)

bot.getPlayerPagesAndExtractStats(playerUrls)
>>>>>>> 8162855eae80c6a1195c93b64c625310f1b51b18
