#!/usr/bin/python

non_sense_list = ["a","the","an","I","am ","is","are","they","them","their","it","here","there","that","and","on","in","of","his","him","with"]

string1 = "Steve Jobs reveals Apple's new spaceship campus, calls it the 'best office building in the world' (video)"

string2 = "Timeline, short biography and detailed biography of Apple CEO Steve Jobs, complete with key people in his life."

def pre_processing(origin):
	# at first we need convert all the words to letter case
	dest = origin.lower()
	dest = dest.replace("'s"," ")
	dest = dest.replace("'"," ")
	dest = dest.replace("("," ")
	dest = dest.replace(")"," ")
	dest = dest.replace("["," ")
	dest = dest.replace("]"," ")
	dest = dest.replace("{"," ")
	dest = dest.replace("}"," ")
	dest = dest.replace(","," ")
	dest = dest.replace("."," ")
	return dest



if  __name__=='__main__':
	my_list = []
	dest = pre_processing(string1).split(" ")
	for word in dest:
		if word not in non_sense_list:
			if len(word) != 0: 
				my_list.append(word.strip())
	print my_list
