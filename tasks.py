import webapp2
import jinja2
import os
import json
import logging
import datetime
from urllib import quote, urlencode
from google.appengine.api import urlfetch
from google.appengine.api import memcache

import headers
import tags
import queries
import configuration

from models import WordcountSummary

def reading_seconds(words):
	return (words / 250) * 60

def read_wordcount(fields):
	return int(fields["wordcount"])

def read_todays_content(page = 1):
	url = "http://beta.content.guardianapis.com/search"

	today = datetime.date.today()

	payload = {
		"page" : str(page),
		"page-size" : "50",
		"format" : "json",
		"show-fields" : "wordcount",
		"tags" : "tone",
		"from-date" : today.isoformat(),
		"api-key" : configuration.lookup('API_KEY'),
		}

	final_url = url + "?" + urlencode(payload)
	#logging.info(final_url)

	result = urlfetch.fetch(final_url, deadline = 9)

	if not result.status_code == 200:
		logging.warning("Failed to read from the Content Api")
		logging.warning('Status code: %d' % result.status_code)
		return

	data = json.loads(result.content)

	api_response = data.get("response", {})

	total_pages = api_response.get("pages", None)

	if not total_pages:
		return

	results = api_response.get("results", [])

	for result in results:
		fields = result.get("fields", {})

		if not 'wordcount' in fields: continue

		path = result["id"]

		live_flag = tags.is_live(result)

		lookup = WordcountSummary.query(WordcountSummary.path == path)

		if lookup.count() > 0:

			record = lookup.iter().next()

			current_wordcount = read_wordcount(fields)

			if not current_wordcount == record.wordcount:
				record.wordcount = current_wordcount
				record.put()

			continue


		WordcountSummary(path = path,
			section_id = result["sectionId"],
			wordcount = read_wordcount(fields),
			iso_published_date = result["webPublicationDate"][:10],).put()

	if not int(total_pages) == page:
		read_todays_content(page + 1)

def create_archive():
	def create_day_info(data):
		date = data[0].iso_published_date

		day = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A")
		wordcount = reduce(lambda acc, item : acc + item.wordcount, data, 0)
		seconds = reading_seconds(wordcount)
		
		summary = (date, day, wordcount, seconds)

		return summary

	now = datetime.date.today()
	logging.info(now.isoformat())
	key = "summary.%s" % now.isoformat()

	summary = memcache.get(key)	

	if not summary:
		data = map(queries.historic_data, [(now - datetime.timedelta(days=i)).isoformat() for i in range(1, 32)])
		data = filter(lambda x: len(x) > 0, data)
		data = map(create_day_info, data)
		memcache.add(key, json.dumps(data), 8 * 60 * 60)


class TodaysCount(webapp2.RequestHandler):
	def get(self):
		
		data = {"status" : "ok"}

		read_todays_content()

		headers.json(self.response)
		self.response.out.write(json.dumps(data))

class CalculateArchive(webapp2.RequestHandler):
	def get(self):
		
		data = {"status" : "ok"}

		create_archive()

		headers.json(self.response)
		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/tasks/today/count', TodaysCount),
	('/tasks/archive', CalculateArchive)],
                              debug=True)