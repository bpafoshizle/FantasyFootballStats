buildADPFileName = function()
{
  paste("adp_", Sys.Date(), ".csv", sep="")
}

getADP = function(format="standard", teams="10")
{
  url = paste("http://fantasyfootballcalculator.com/adp_csv.php?format=", format, "&teams=", teams, sep="")
  destFile = buildADPFileName()
  download.file(url=url, destfile=destFile)
  
  adp <<- read.csv(destFile, skip=4, stringsAsFactors=F)
  adp <<- adp[-nrow(adp),]
  adp$ADP <<- as.numeric(adp$ADP)
}

#getADP()
main = function()
{
  getADP()
}
