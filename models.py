from google.appengine.ext import ndb

class Configuration(ndb.Model):
	key = ndb.StringProperty()
	value = ndb.StringProperty()

class WordcountSummary(ndb.Model):
	path = ndb.StringProperty()
	wordcount = ndb.IntegerProperty()
	section_id = ndb.StringProperty()
	iso_published_date = ndb.StringProperty()