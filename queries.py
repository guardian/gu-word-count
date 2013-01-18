from models import WordcountSummary

def historic_data(date):
	return [s for s in WordcountSummary.query(WordcountSummary.iso_published_date == date)]