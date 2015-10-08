Advanced database systems, homework 1

1. authors:
Zichen Chao (zc2321)
Hui Zou (hz2361)

2. submitted files:
main.py  // the main file
DocVec.py  // implement TF-IDF algorithm
BingSearch.py  // connect Bing API 
stopwords.txt
transcript.txt
readme.txt

3. to run our program:
python main.py <account key> <target> <initial query>

for example:
python main.py Ubg5f7OtyJkNHu69me7rh1pp22lXCcaXDDuCnYLAoaU 0.9 'Taj mahal'

4. description:
our codes implement the TFIDF algorithm taught in class and use relevance feedback to make the query expansion. After we get the results from Bing API, we invoke users to judge the relevance of each result, simplify the documents to drop off stop words and punctuations, and then categorize them into relevant or non-relevant fields. We calculate the TF and IDF with the title and description of each result, and make an average calculation of the vector value for the relevant/non-relevant fields respectively. Finally we apply the "The underlying theory" and make a vector difference of those two fields, extract two words with highest vector value, and append them to the original query to form the new query. When the target value is not achieved, we continue the above steps with the new query.

5. query modification method:
we maintain the data structure to record TF value and DF value for each term appeared once in the documents. The TF(ij) represents number of times term t(i) occurs in document d(j). And the DF(i) represents the number of documents in which term t(i) occurs. Then we apply the formula:
W(ij) = TF(ij) * log(#documents / DF(i))
to get the weight of each term related to each document.
Then we use the formula as shown in reference (2) to get the weight vector with weight value of each word. The basic idea here is to calculate the average value of each term(word) in the relevant/non-relevant class respectively as their weight, and make a vector subtraction, leverage the term/word weight in relevant class to subtract the same term weight in non-relevant class to get the final term weight.   
The terms/words with highest weight value are considered first as good candidates for query expansion. For each iteration we will add two new words.

6. Bing Search Account Key:
Ubg5f7OtyJkNHu69me7rh1pp22lXCcaXDDuCnYLAoaU

7. references:
(1) "Introduction to Information Retrieval" by Christopher, Prabhakar, Hinrich. Chapter 9. ISBN:  0521865719
(2) The formula to calculate vector relation between relevant documents and non-relevant documents: "Introduction to Information Retrieval", by Christopher, Prabhakar, Hinrich. Page 181, formula (9.2) Web link: http://nlp.stanford.edu/IR-book/pdf/09expand.pdf (cited 10/07/2015)
