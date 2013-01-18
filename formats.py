import datetime

def jsonp(request, json_string):
	if request.get("callback"):
		return "%s(%s)" % (request.get("callback"), json_string)
	return json_string

def ordinal(day):
	if 4 <= day <= 20 or 24 <= day <= 30:
		return "th"
	return ["st", "nd", "rd"][day % 10 - 1]

def fancy_date(date):
	dt = datetime.datetime.strptime(date, "%Y-%m-%d")
	suffix = ordinal(dt.day)
	format = "%%d%s %%B %%Y" % suffix
	return dt.strftime(format)

