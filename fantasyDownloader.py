from ProFootballRefDownloader import ProFootballRefDownloader

bot = ProFootballRefDownloader()


for url in bot.getYearUrlsFromYearsPage(5):
	print url

