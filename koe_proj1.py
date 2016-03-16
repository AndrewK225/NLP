#!/cygdrive/c/python27/python


import argparse,time
from nltk.tokenize import RegexpTokenizer



def main(args):
	cat2feats = {}
	vocab = {}
	tokenizer = RegexpTokenizer(r'\w+') 
	test_list = open(args['test'],'rb')
	train_list = open(args['train'],'rb')

	lemmatized = []
	
	#train
	start = time.time()
	for train_file in train_list:	
		line = train_file.split()
		if line[1] not in cat2feats:
			cat2feats[line[1]] = {}  # add the category to the dictionary
		
		tf = open(line[0],'rb') #open each file		
		tokens = tokenizer.tokenize(tf.read()) 

	
		for word in tokens:
			#keep track of entire vocab
			try:
				vocab[word] += 1
			except KeyError:
				vocab[word] = 1
				
			if word.lower() in cat2feats[line[1]]: #line[1] is the category
				cat2feats[line[1]][word.lower()] += 1
			else:
				cat2feats[line[1]][word.lower()] = 1
	end = time.time()
	print(end-start)	
	exit()

	#testing
	
	for test_file in test_list:
		test = open(test_file)
		toks = tokenizer.tokenize(test.read())
		for cat in cat2feats:
			if word in cat2feats[cat]:
						
	
			


if __name__ == "__main__":

	#get the files that list the paths to files
	parser = argparse.ArgumentParser(description="Text Classification")
	parser.add_argument('--train',help="list of training files",required=True)
	parser.add_argument('--test',help="list of test files",required=True)
	args = vars(parser.parse_args())
	print("starting")
	main(args)
