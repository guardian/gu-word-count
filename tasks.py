import webapp2
import jinja2
import os
import json
import logging
from urllib import quote, urlencode
from google.appengine.api import urlfetch

import headers

from models import WordcountSummary

def read_todays_content(page = 1):
	url = "http://content.guardianapis.com/search"

	payload = {"page" : str(page),
		"page-size" : "50",
		"format" : "json",
		"show-fields" : "wordcount",
		"date-id" : "date/today",}

	final_url = url + "?" + urlencode(payload)
	logging.info(final_url)

	result = urlfetch.fetch(final_url, deadline = 9)

	if not result.status_code == 200:
		logging.warning("Failed to read from the Content Api")
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

		lookup = WordcountSummary.query(WordcountSummary.path == path)

		if lookup.count() > 1: continue

		WordcountSummary(path = path,
			section_id = result["sectionId"],
			wordcount = int(fields["wordcount"]),
			iso_published_date = result["webPublicationDate"][:10],).put()

	if not int(total_pages) == page:
		read_todays_content(page + 1)



class TodaysCount(webapp2.RequestHandler):
	def get(self):
		
		data = {"status" : "ok"}

		read_todays_content()

		headers.json(self.response)
		self.response.out.write(json.dumps(data))

app = webapp2.WSGIApplication([('/tasks/today/count', TodaysCount)],
                              debug=True)