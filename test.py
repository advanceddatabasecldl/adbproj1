import sys

class word(object):
	def __init__(self,name=None,value=0,inverted_list=[]):
		self.name = name
		self.value = value
		self.inverted_list = inverted_list


#test the way to sort a object in python
if __name__ == "__main__":
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
