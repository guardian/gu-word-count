import webapp2
import jinja2
import os
import json
import logging
import collections
import datetime

from urllib import quote, urlencode
from google.appengine.api import urlfetch
from google.appengine.api import memcache

import queries
import formats

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

def reading_seconds(words):
	return (words / 250) * 60

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('index.html')
		
		template_values = {}

		self.response.out.write(template.render(template_values))

class ArchivePage(webapp2.RequestHandler):
	def get(self, date):
		logging.info(date)
		template = jinja_environment.get_template('archive.html')

		data = queries.historic_data(date)

		logging.info(data)

		wordcount = reduce(lambda acc, item : acc + item.wordcount, data, 0)

		def section_count(counter, item):
			counter[item.section_id] += item.wordcount
			return counter

		section_counts = reduce(section_count, data, collections.Counter())

		section_data = [(section_id, section_counts[section_id], reading_seconds(section_counts[section_id])) for section_id in section_counts.keys()]

		sorted_section_data = sorted(section_data, reverse = True, key = lambda x : x[1])
		
		template_values = {
			'date' : formats.fancy_date(date),
			'data' : data,
			'wordcount' : "{:,d}".format(wordcount),
			'reading_seconds' : reading_seconds(wordcount),
			'sections' : sorted_section_data
		}

		self.response.out.write(template.render(template_values))

class ArchiveListingPage(webapp2.RequestHandler):
	def get(self):

		template = jinja_environment.get_template('archive-listing.html')
		template_values = {}

		now = datetime.date.today()
		key = "summary.%s" % now.isoformat()

		summary = memcache.get(key)

		if summary:
			template_values['days'] = json.loads(summary)

		self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage),
	('/archive/(\d\d\d\d-\d\d-\d\d)', ArchivePage),
	('/archive', ArchiveListingPage),],
                              debug=True)