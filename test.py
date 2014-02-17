#! /usr/bin/python
'''
Created on Feb 3, 2014

@author: Milannic
'''

from __builtin__ import len
import sys
import urllib
import urllib2
import re
import json
#from locale import str

result_list = None
relavant_list = []
irrelavant_list = []
dict_table = {}
query_list = []
query = ""
beta = 0.85
gamma = 1-beta
non_sense_list = ["to","a","the","an","i","am","is","are","they","them","their","it","here","there","that","and","on","in","of","his","him","with","was","were"]
symbol_list = ["\"",".",",","}","{","]","[",")","(","\'","\'s",":"]

def pre_processing(origin):
	global non_sense_list
	# at first we need convert all the words to letter case
	dest = origin.lower()
	for symbol in symbol_list:
		dest = dest.replace(symbol," ")
	return dest

def iteration_result():
	global relavant_list
	global irrelavant_list
	global dic_table
	global query_list
	global query
	global beta
	global gamma
	dic_table = {}
	for relavant_result in relavant_list:
		ratio = len(relavant_result)
		if ratio != 0:
			for relavant_word in relavant_result:
					new_value = beta/ratio
					if dic_table.has_key(relavant_word):
						dic_table[relavant_word] = dic_table[relavant_word] + new_value 
					else:
						dic_table[relavant_word] = new_value 
	for irrelavant_result in irrelavant_list:
		ratio = len(irrelavant_result)
		if ratio != 0 :
			for irrelavant_word in irrelavant_result:
					new_value = -gamma/ratio
					if dic_table.has_key(irrelavant_word):
						dic_table[irrelavant_word] = dic_table[irrelavant_word] + new_value 
					else:
						dic_table[irrelavant_word] = new_value 
	sorted_list = sorted(dic_table.items(), key=lambda x: x[1])
	if len(sorted_list) == 0:
		raise Exception("why there is no new word?")
	elif len(sorted_list) == 1:
		new_word = sorted_list.pop()[0]
		query = query + " " + new_word 
		query_list.append(new_word)
	else: 
		new_word = sorted_list.pop()[0]
		query = query + " " + new_word 
		query_list.append(new_word)
		new_word = sorted_list.pop()[0]
		query = query + " " + new_word 
		query_list.append(new_word)

def cal_precision(result_list):
	global relavant_list
	global irrelavant_list
	relavant_list = []
	irrelavant_list = []
	for index,result in zip(range(len(result_list)),result_list):
		print "the number ",index, " result"
		#print type(result['Description'])
		result['Description'] = result['Description'].encode('ascii','ignore')
		result['Title'] = result['Title'].encode('ascii','ignore')
		#print type(result['Description'])
		print "Title : ",result['Title']
		print "Description : ",result['Description']
		print "Url : ",result['Url']
		print "is this result relavant to your query? Yes Or No "
		new_string = pre_processing(result['Description'] + " " +result['Title'])
		print new_string
		new_list = []
		print "after the pre processing, the string will be:"
		for split_word in new_string.split(" "):
			if split_word not in non_sense_list and split_word not in query_list and len(split_word) !=0  and split_word != '-':
				new_list.append(split_word)
		print new_list
		answer = raw_input("------>")
		if re.match(".*[yY].*",answer) != None:
			relavant_list.append(new_list)
		elif re.match(".*[nN].*",answer)!=None:
			irrelavant_list.append(new_list)
		else:
			raise Exception("cannot recognize the parameter you input")
	rela_num = len(relavant_list)
	return rela_num
	
			

def main():
	global query
	global query_list
	query = "steve jobs"
	query_list = query.lower().split()
	print query_list
	precision10 = 0.9
	result_list = bing_search(query, 'Web')
	#print result_list
	while True:
		if(len(result_list) < 10):
			raise Exception("less than 10 records found")
		rela_num=cal_precision(result_list)
		print  rela_num
		if(precision10 <= rela_num/10):
			break
		elif(rela_num == 0):
			raise Exception("no related queries found")
		iteration_result()
		result_list = bing_search(query, 'Web')
		
		


def bing_search(query, search_type):
	print "current query is ", query
	#search_type: Web, Image, News, Video
	key= 'OWeD/fOooFJbAKRI1mxcpBlwof/LyYLz9nQ7lSBIjC8'
	query = urllib.quote(query)
	# create credential for authentication
	user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
	credentials = (':%s' % key).encode('base64')[:-1]
	auth = 'Basic %s' % credentials
	url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'%27&$top=10&$format=json'
	request = urllib2.Request(url)
	request.add_header('Authorization', auth)
	request.add_header('User-Agent', user_agent)
	request_opener = urllib2.build_opener()
	response = request_opener.open(request) 
	response_data = response.read()
	json_result = json.loads(response_data)
	result_list = json_result['d']['results']
# field information : Description, Title,Url
#Specify the 
	return result_list


class word(object):
	def __init__(self,name=None,value=0,inverted_list=[]):
		self.name = name
		self.value = value
		self.inverted_list = inverted_list


#test the way to sort a object in python
if __name__ == "__main__":
<<<<<<< HEAD
	main()

__comment = '''
{u'Description': u'30 years later, Steve Jobs still inspires Thirty years after Jobs introduced the Macintosh computer at a gathering in Boston, his presentation and passion ...', u'Title': u'30 years later, Steve Jobs still inspires - Business - The ...', u'Url': u'http://www.bostonglobe.com/business/2014/02/03/years-later-steve-jobs-still-inspires/wnKSCXi89VDX2LaFFAgr4M/story.html', u'__metadata': {u'type': u'WebResult', u'uri': u"https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query='steve jobs'&$skip=8&$top=1"}, u'DisplayUrl': u'www.bostonglobe.com/business/2014/02/03/years-later-steve-jobs...', u'ID': u'655ec1a5-4585-40f4-bfb8-2b591cd8ede2'}
'''
=======
	word1 = word("hello",3,[1,7,5])
	word2 = word("fuck",7,[2,6,5])
	word3 = word("kk",5,[2,6,5])
	pos_word_list = []
	pos_word_list.append(word1)
	pos_word_list.append(word2)
	pos_word_list.append(word3)
	print pos_word_list[1].name
	pos_word_list.sort(key = lambda word: word.value)
	print pos_word_list
	print pos_word_list[1].name
	for word in pos_word_list:
		print word.value
>>>>>>> f8d28640dba7d39733430aa41d009b4c8c0bad23
