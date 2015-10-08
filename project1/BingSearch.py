import urllib2
import base64
import json
class BingSearch(object):
	"""docstring for ClassName"""
	def __init__(self, accountKey, query):
		self.rootUrl = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27" + query + "%27&$top=10&$format=json"
		accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
		self.headers = {'Authorization': 'Basic ' + accountKeyEnc}

	def getURL(self):
		return self.rootUrl

	def search(self):
		req = urllib2.Request(self.rootUrl, headers = self.headers)
		response = urllib2.urlopen(req)
		content = response.read()

		# content contains the xml/json response from Bing.
		results = json.loads(content)['d']['results']

		# 'Content':it['content']
		return [{'Title':it['Title'], 'Url':it['Url'], 'Summary':it['Description']} for it in results]
