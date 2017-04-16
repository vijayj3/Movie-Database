from __future__ import unicode_literals
from urllib2 import Request, urlopen, URLError
import json
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

API_KEY = "65352c83b3ec57a8a7009a4a95ddaef0"
BASE_URL = "https://api.themoviedb.org/3"


from spacy.en import English
parserEN = English()

class MovieAPI():
	
	def __init__(self, phrase):
		self.phrase = phrase
		
	def parser(self):
		parsedEx = parserEN(unicode(self.phrase))

		person = []
		year = None
		for token in parsedEx:
			if token.ent_type_ == "PERSON":
				person.append(token.orth_)
			elif token.ent_type_ == "DATE":
				year= token.orth_

		if not person:
			person = None
		else:
			person = " ".join(person)


		return self.discoverQuery(year= year, person = person)

	def searchPersonQuery(self,person):
		person = '+'.join(person.split())
		search_url = BASE_URL + "/search/person?api_key=" + API_KEY
		search_url = search_url + "&query=" + person

		# logging.debug('search URL: %s', search_url)
		results_json = self.fetchJSONFromURL(search_url)
		if not results_json['results']:
			result = -1
		else:
			result = results_json['results'][0]['id']

		return result


	def discoverQuery(self,year,person):

		discQuery = BASE_URL + "/discover/movie?api_key=" + API_KEY
		discQuery = discQuery +  "&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1"
		
		if person== None and year == None:
			print "You need to enter a valid year and person"
			return None
		elif year != None and person == None:
			year_url = "&primary_release_year=" + str(year)
			discQuery += year_url
		elif year == None and person != None:
			person_url = "&with_cast=" + str(self.searchPersonQuery(person))
			discQuery += person_url
		elif year != None and person != None:
			year_url = "&primary_release_year=" + str(year)
			person_url = "&with_cast=" + str(self.searchPersonQuery(person))
			discQuery = discQuery + year_url + person_url

		logging.debug("Discovery Query: %s", discQuery)
		results_json = self.fetchJSONFromURL(discQuery)
		if not results_json['results']:
			lst = []
			lst.append("Sorry No results available")
		else:
			results = results_json['results']
			lst = []
			for result in results:
				lst.append(result['title'])
			
		return lst

	def fetchJSONFromURL(self,url):
		request = Request(url)
		try:
			response = urlopen(request)
			data = response.read()
			results_json = json.loads(data)
		except URLError, e:
			print str(e)

		return results_json

#######################################################################

# phrase = raw_input(INPUT_SYM)
# print searchPersonQuery(phrase)

# phrase = raw_input(INPUT_SYM)
# print discoverQuery('1980', 'Tom Hanks')

##########################################################################


# print discoverQuery(year = year,person = person)

