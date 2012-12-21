import webapp2
import jinja2
import os
import json
import logging
import datetime

from urllib import quote, urlencode
from google.appengine.api import urlfetch

import headers

from models import WordcountSummary

def today():
	today = datetime.date.today()
	return today.isoformat()

def generate_totals(today):
	query = WordcountSummary.query(WordcountSummary.iso_published_date == today)

	totals = {"wordcount" : 0, "sections" : {}}
	for result in query:
		totals["wordcount"] += result.wordcount

	return totals

def reading_time(data):
	return {"reading_minutes" : data['wordcount'] / 250 }

class Today(webapp2.RequestHandler):
	def get(self):

		date = today()
		
		data = {"date" : date}

		data.update(generate_totals(date))

		data.update(reading_time(data))

		headers.json(self.response)
		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/api/today', Today)],
                              debug=True)