#!/cygdrive/c/python27/python

import argparse,time,math
from nltk.tokenize import RegexpTokenizer


def main(args):
	cat2feats = {}
	vocab = {}
	words_in_cat = {}
	final_probs = {}
	prob_per_cat = {}
	files_per_cat = {}
	tokenizer = RegexpTokenizer(r'\w+') 
	test_list = open(args['test'],'rb')
	train_list = open(args['train'],'rb')
	alpha = 0.05
	
	#train
	for train_file in train_list:	
		line = train_file.split()
		prob_per_cat[line[1]] = 0.0
		try:
			files_per_cat[line[1]] += 1.0
		except KeyError:
			files_per_cat[line[1]] = 1.0

		if line[1] not in cat2feats:
			cat2feats[line[1]] = {}  # add the category to the dictionary
		
		tf = open(line[0],'rb') #open each file		
		tokens = tokenizer.tokenize(tf.read()) 
	
		for word in tokens:
			#keep track of entire vocab
			try:
				vocab[word] += 1.0
			except KeyError:
				vocab[word] = 1.0
				
			if word.lower() in cat2feats[line[1]]: #line[1] is the category
				cat2feats[line[1]][word.lower()] += 1.0
			else:
				cat2feats[line[1]][word.lower()] = 1.0

	#total number of words in each cat	
	for cat in cat2feats:
		words_in_cat[cat] = sum(cat2feats[cat].itervalues())
	
	
	outfile = open(args['out'],'wb')
	#testing
	for test_file in test_list:
		for cat in prob_per_cat:
			prob_per_cat[cat] = 0.0
		test = open(test_file.rstrip(),'rb')
		toks = tokenizer.tokenize(test.read())
		for word in toks:
			for cat in cat2feats:
				try:
					prob_per_cat[cat] += math.log((cat2feats[cat][word.lower()] + alpha)/(words_in_cat[cat] + alpha*len(vocab)))
				except KeyError: #word not seen before
					prob_per_cat[cat] += math.log(alpha/(words_in_cat[cat] + alpha*len(vocab)))

		
		for cat in prob_per_cat:
			prob_per_cat[cat] += math.log((files_per_cat[cat]/sum(files_per_cat.itervalues())))


		prob = float("-inf")
		ans = ""		
		for cat in prob_per_cat:
			if prob_per_cat[cat] > prob:
				prob = prob_per_cat[cat]
				ans = cat
			else:
				continue

		outfile.write(test_file.rstrip() + " "+ ans + "\n")
						
	
if __name__ == "__main__":
	#get the files that list the paths to files
	parser = argparse.ArgumentParser(description="Text Classification")
	parser.add_argument('--train',help="list of training files",required=True)
	parser.add_argument('--test',help="list of test files",required=True)
	parser.add_argument('--out',help="name of output file", required=True)
	args = vars(parser.parse_args())
	main(args)
