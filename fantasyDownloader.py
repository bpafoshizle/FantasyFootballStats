from ProFootballRefBot import ProFootballRefBot

bot = ProFootballRefBot()

#for url in bot.getYearUrlsFromYearsPage(5):
#	print url


#for url in bot.getFantasyPlayerUrlsByYear(numPlayers=50):
#	print url

#bot.downloadPlayerPagesForYear('2013')
bot.downloadGamelogPagesForYear('2013')

#playerUrls = bot.getPlayerGamelogUrls(numYears=2,numPlayers=1)
#bot.getPlayerPagesAndExtractStats(playerUrls)
