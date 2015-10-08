import math
class FeedbackDocVec(object):
	"""docstring for ClassName"""
	def __init__(self, q):
		self.dic = []  # dic for the doc collection
		self.n_docs = 0  # number of total docs
		self.r_tf = [[], []]  # tf vectors for relevant and irrelevant docs
		self.df = {}  # df vector
		self.q = [q]  # query list
		self.w_id = {}  # indicate the id for each word

	# update the keys of dics, return the list of dic for this doc
	# and the list of newly added words
	def update_key(self, parsed):
		dic_for_doc = []
		newly_added_dic = []
		for w in parsed:
			if not w in self.dic:
				self.df[w] = 0
				self.dic.append(w)
				self.w_id[w] = len(self.dic) - 1
				newly_added_dic.append(w)

			if not w in dic_for_doc:
				dic_for_doc.append(w)
		return dic_for_doc, newly_added_dic

	# eliminate punctuations
	def clean_doc(self, doc):
		ans = ''
		for w in doc:
			if w in [',', '.', '?', '!', '\'', '#', ':', '|', '\"']:
				ans += ' '
			else:
				ans += w
		return ans

	# eliminate stopwords
	def simplify_doc(self, doc):
		ans = ''
		f = open("stopwords.txt","r")
		stopwords = []
		for word in f:
			stopwords.append(word.rstrip())
		words = doc.split()
		for w in words:
			if w in stopwords:
				ans += ' '
			else:
				ans += w + ' '
		return ans

	# feed new doc into the dic collection, doc is a string
	def feed_doc(self, doc, rid):
		doc = doc.lower()
		doc = self.clean_doc(doc)
		doc = self.simplify_doc(doc)
		self.n_docs += 1
		parsed = doc.split()

		# update key of dic
		dic_for_doc, newly_added_dic = self.update_key(parsed)

		# update document frequency for w
		for w in dic_for_doc:
			self.df[w] += 1

		# update term frequencies for existed docs
		added = [0 for w in newly_added_dic]
		for r in range(2):
			for doc_tf in self.r_tf[r]:
				doc_tf += added

		# calculate term frequencies for newly added doc
		self.r_tf[rid].append([0 for w in self.dic])
		for w in parsed:
			self.r_tf[rid][-1][self.w_id[w]] += 1

	# feed new docs into the doc collection, docs is a list of string
	def feed_docs(self, docs, rid):
		for doc in docs:
			self.feed_doc(doc, rid)

	# get tf-idf vectors for each class
	def get_vec_for_rdocs(self, rid):
		vecs = [[0 for w in self.dic] for it in self.r_tf[rid]] 
		for (id, tf) in enumerate(self.r_tf[rid]):
			for j in range(len(self.dic)):
				vecs[id][j] = tf[j] * math.log(self.n_docs / float(self.df[self.dic[j]]))
		return vecs

	# calculate average tf-idf vector for each class
	def average_vecs(self, vecs):
		n = len(self.dic)
		ave = [0 for i in range(n)]
		for vec in vecs:
			for i in range(n):
				ave[i] += vec[i]
		return [ave[i] / float(len(vecs)) for i in range(n)]

	# calculate difference and update query
	def cal_dif(self):
		vecs = [self.get_vec_for_rdocs(rid) for rid in range(2)]
		aves = [self.average_vecs(vecs[rid]) for rid in range(2)]
		
		dif = [(aves[1][i] - aves[0][i]) if (aves[1][i] - aves[0][i] > 0) else 0 for i in range(len(self.dic))]

		# find two words with the highest tf-idf difference
		pos1 = dif.index(max(dif))
		while (self.dic[pos1] in self.q):
			dif[pos1] = 0
			pos1 = dif.index(max(dif))
		dif[pos1] = 0

		pos2 = dif.index(max(dif))
		while (self.dic[pos2] in self.q):
			dif[pos2] = 0
			pos2 = dif.index(max(dif))

		# update query
		self.q.extend([self.dic[pos1], self.dic[pos2]])
		return self.dic[pos1], self.dic[pos2]
