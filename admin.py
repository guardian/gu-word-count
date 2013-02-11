import webapp2
import jinja2
import os
import json
import logging

import queries
import formats

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('admin.html')
		
		template_values = {}

		self.response.out.write(template.render(template_values))


app = webapp2.WSGIApplication([('/admin', MainPage),],
                              debug=True)