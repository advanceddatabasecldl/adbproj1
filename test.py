#! /usr/local/bin/python

'''
Created on Feb 3, 2014

@author: Milannic
'''

import	argparse 
import base64
import urllib2
import re
import json
import uuid
from __builtin__ import str
#import en
#from locale import str

iter_round = 0
accountKey = ''
precision10 = 0
result_list = None
relavant_list = []
irrelavant_list = []
dict_table = {}
query_list = []
query = ""
beta = 0.85
gamma = 1-beta
output_file_desp = None
non_sense_list = ["us","our","to","a","the","an","i","am","is","are","they","them","their","it","here","there","that","and","on","in","of","his","him","with","was","were"]
symbol_list = ["\"",".",",","}","{","]","[",")","(","\'","\'s",":","|","&","*"]

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
# 	elif len(sorted_list) == 1:
	else :
		new_word = sorted_list.pop()[0]
		query = query + " " + new_word 
		query_list.append(new_word)
# 	else: 
# 		new_word = sorted_list.pop()[0]
# 		query = query + " " + new_word 
# 		query_list.append(new_word)
# 		new_word = sorted_list.pop()[0]
# 		query = query + " " + new_word 
# 		query_list.append(new_word)

def cal_precision(result_list):
	global relavant_list
	global irrelavant_list
	global iter_round
	global output_file_desp
	
	relavant_list = []
	irrelavant_list = []
	for index,result in zip(range(len(result_list)),result_list):
		print "the number ",index, " result"
		output_file_desp.write("the number "+str(index) + " result\n\n")
		
		result['Description'] = result['Description'].encode('ascii','ignore')
		result['Title'] = result['Title'].encode('ascii','ignore')
		result['Url'] = result['Url'].encode('ascii','ignore')
		
		print "Title : ",result['Title']
		output_file_desp.write("Title : " + result['Title']+'\n\n')
		
		print "Description : ",result['Description']
		output_file_desp.write("Description : " + result['Description']+'\n\n')
		
		print "Url : ",result['Url']
		output_file_desp.write("Url : " + result['Url']+'\n\n')
		
		print "is this result relavant to your query? Yes Or No "
		new_string = pre_processing(result['Description'] + " " +result['Title'])
		new_list = []
		for split_word in new_string.split(" "):
			if split_word not in non_sense_list and split_word not in query_list and len(split_word) !=0  and split_word != '-' :
				new_list.append(split_word)
		answer = raw_input("------>")
		if re.match(".*[yY].*",answer) != None:
			relavant_list.append(new_list)
			output_file_desp.write("this result is related, yes\n\n")
		elif re.match(".*[nN].*",answer)!=None:
			irrelavant_list.append(new_list)
			output_file_desp.write("this result is not related, no\n\n")
		else:
			output_file_desp.write("cannot recognize the parameter you input")
			output_file_desp.close()
			raise Exception("cannot recognize the parameter you input")
	rela_num = len(relavant_list)
	output_file_desp.write("in this iteration, the realted number of result is "+str(rela_num)+'\n\n')
	return rela_num
	
			

def main():
	
	global query
	global query_list
	global accountKey
	global precision10
	global iter_round
	global output_file_desp
	
	output_file_desp = open("transcript_"+str(uuid.uuid1())[0:6],'w')
	
	#parse the parameter
	my_parse = argparse.ArgumentParser(description = "this is a test")
	my_parse.add_argument("-k","--key",dest = "my_key",type=str,default = "OWeD/fOooFJbAKRI1mxcpBlwof/LyYLz9nQ7lSBIjC8")
	my_parse.add_argument("-q","--query",dest = "init_query",type=str,default ='steve jobs')
	my_parse.add_argument("-p","--precision",dest = "precision10",type=float,default = 0.9)
	my_para = my_parse.parse_args()
	
	
	accountKey = my_para.my_key
	query = my_para.init_query
	precision10 = my_para.precision10
	query_list = query.lower().split()
	
	while True:
		output_file_desp.write("round "+str(iter_round)+'\n\n')
		output_file_desp.write("current query is "+query+'\n\n')
		result_list = bing_search(query)
		if(len(result_list) < 10):
			output_file_desp.write("less than 10 records found")
			output_file_desp.close()
			raise Exception("less than 10 records found")
		rela_num=cal_precision(result_list)
		#print  rela_num
		if(precision10 <= float(rela_num)/10):
			break
		elif(rela_num == 0):
			output_file_desp.write("no related queries found")
			output_file_desp.close()
			raise Exception("no related queries found")
		iteration_result()
		iter_round += 1
		
	output_file_desp.write("have reached the required precision10 \n\n")
	output_file_desp.close()
		


def bing_search(query):
	# create credential for authentication
	inner_query = urllib2.quote(query)
	bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'+inner_query+'%27&$top=10&$format=json'
	accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
	headers = {'Authorization': 'Basic ' + accountKeyEnc}
	req = urllib2.Request(bingUrl, headers = headers)
	response = urllib2.urlopen(req)
	content = response.read()
	#print type(content)
	#content contains the xml/json response from Bing. 
	#then parse it 
	json_result = json.loads(content)
	#just get the field we need for parsing
	# field information : Description, Title,Url
	result_list = json_result['d']['results']
	#return it
	return result_list


if __name__ == "__main__":
	main()

