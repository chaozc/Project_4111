import urllib2
import base64
import json
class BingSearch(object):
	"""docstring for ClassName"""
	def __init__(self, accountKey, query, precision):
		self.rootUrl = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27"+query+"%27&$top=10&$format=json"
		print self.rootUrl
		accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
		self.headers = {'Authorization': 'Basic ' + accountKeyEnc}
	def search(self):
		req = urllib2.Request(self.rootUrl, headers = self.headers)
		response = urllib2.urlopen(req)
		content = response.read()
		#content contains the xml/json response from Bing. 
		results = json.loads(content)['d']['results']
		"""
		for it in results:
			urlreq = urllib2.Request(it['Url'])
			res = urllib2.urlopen(urlreq)
			it['content'] = res.read()
		"""
		#'Content':it['content']
		return [{'Title':it['Title'], 'Url':it['Url'], 'Summary':it['Description']} for it in results]

if __name__ == "__main__":
	search = BingSearch('bTbLwNb1w9U/wXfcpBAww4VqVBOWgkq7DxqIja6wsKU', 'basketball', 0.9)
	print search.search()