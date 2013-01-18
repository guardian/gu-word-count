import webapp2
import jinja2
import os
import json
import logging
import collections

from urllib import quote, urlencode
from google.appengine.api import urlfetch

import queries

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

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

		def reading_seconds(words):
			return (words / 250) * 60

		wordcount = reduce(lambda acc, item : acc + item.wordcount, data, 0)

		def section_count(counter, item):
			counter[item.section_id] += item.wordcount
			return counter

		section_counts = reduce(section_count, data, collections.Counter())

		section_data = [(section_id, section_counts[section_id], reading_seconds(section_counts[section_id])) for section_id in section_counts.keys()]

		sorted_section_data = sorted(section_data, reverse = True, key = lambda x : x[1])
		
		template_values = {
			'date' : date,
			'data' : data,
			'wordcount' : wordcount,
			'reading_seconds' : reading_seconds(wordcount),
			'sections' : sorted_section_data
		}

		self.response.out.write(template.render(template_values))



app = webapp2.WSGIApplication([('/', MainPage),
	('/archive/(\d\d\d\d-\d\d-\d\d)', ArchivePage)],
                              debug=True)