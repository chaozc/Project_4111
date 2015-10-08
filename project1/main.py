from BingSearch import BingSearch
from DocVec import *
import sys

if __name__ == "__main__":
	if (len(sys.argv) < 4):
		print 'lack argements, please input account key, target, and query'
		sys.exit(0)
	accountKey = sys.argv[1]
	precision = float(sys.argv[2])
	raw_q = sys.argv[3].split()
	q = '%20'.join(raw_q)
	fb = FeedbackDocVec(q)
	cr = 1
	firstIter = True;
	while cr < 10 * precision and cr > 0:
		cr = 0
		BS = BingSearch(accountKey, q)
		results = BS.search()
		# when search results are less than 10 in first iteration, stop
		if (firstIter and len(results) < 10):
			print 'Below desired precision, but can no longer augment the query'
			break
		print 'Parameters:'
		print 'Client key =', accountKey
		print 'Query =', ' '.join(raw_q)
		print 'Precision =', precision
		print 'URL:', BS.getURL()
		print 'Total no of results:', len(results)
		print 'Bing Search Results:'
		print '====================='
		for (id, result) in enumerate(results):
			print 'Result', id + 1
			print '['
			for key in ['Url', 'Title', 'Summary']:
				print '', key, ':', result[key].encode("utf-8")
			print ']'
			feedback = raw_input('Relevant (Y/N)?')
			print ''
			if feedback in ['Y', 'y']:
				fb.feed_doc(result['Title'] + result['Summary'], 1)
				cr += 1
			else:
				fb.feed_doc(result['Title'] + result['Summary'], 0)
		# when no relevance are found, stop
		if (cr == 0):
			print 'Below desired precision, but can no longer augment the query'
			break
		firstIter = False
		print '================='
		print 'FEEDBACK SUMMARY'
		print 'Query:', ' '.join(fb.q)
		print 'precision', float(cr) / 10
		if (cr >= precision * 10):
			print 'Desired precision reached, done'
			break
		else:
			print 'Still below the desired precision of', precision
		newq1, newq2 = fb.cal_dif()
		q = q + '%20' + newq1 + '%20' + newq2
		print 'Augmenting by', newq1, newq2
