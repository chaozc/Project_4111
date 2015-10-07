from BingSearch import BingSearch
from DocVec import *
if __name__ == "__main__":
	q = 'musk'
	fb = FeedbackDocVec(q)
	cr = 1
	while cr < 9 and cr > 0:
		print 'Query:', q
		cr = 0
		BS = BingSearch('bTbLwNb1w9U/wXfcpBAww4VqVBOWgkq7DxqIja6wsKU', q, 0.9)
		results = BS.search()
		for (id, result) in enumerate(results):
			print 'Result', id+1
			print '['
			for key in ['Url', 'Title', 'Summary']:
				print '', key, ':', result[key]
			print ']'
			feedback = raw_input('Relevant (Y/N)?')
			print ''
			if feedback in ['Y', 'y']:
				fb.feed_doc(result['Title']+result['Summary'], 1)
				cr += 1
			else:
				fb.feed_doc(result['Title']+result['Summary'], 0)
		newq = fb.cal_dif()
		#print cc
		#break
		q = q+'%20'+newq