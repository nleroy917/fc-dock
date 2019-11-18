#!/usr/bin/python3

import sys
import os
import numpy as np

"""
This is a python script which searches the loop-modeling output directory for the highest scoring loops - those that have the lowest energy conformations according to the Rosetta REF2015 score function

We can let it identify the best loops, and it will output the file names to a separate text file which will be read by the shell script to choose the loops to be docked.
"""

def find_columns(headers):
	"""
	This function accepts the header line of the score file as input, and will return a dictionary that assocaites header/column names with their repsecitve indices
	This is to help make the code more abstract and prevent future issues/hardcoding
	"""

	index_store = {}

	# Split the header line of the file by white space... iterate through each header, and store the name and index in the dictionary
	for header, i in zip(headers.split(),range(len(headers.split()))):
		index_store[header]=i

	# return this dictionary
	return index_store



if __name__ == "__main__":

	loops = {} # Initialize the loops dictionary
	num_loops = int(sys.argv[1]) # extract the number of top-scoring loops to output from the command line

	score_file = "./output_files/score.sc"

	with open(score_file,'r') as f:
		contents = f.readlines()
		index_store = find_columns(contents[1])
		for line in contents[2:]:
			line = line.split()
			print(line)
			print('File:',line[index_store['description']],'|','Score:',line[index_store['total_energy']])
			loops[line[index_store['description']]] = float(line[index_store['total_energy']])

	# Sort the dictionary
	loops_sorted = sorted(loops.items(), key=lambda x: x[1])

	for loop in loops_sorted:
		print(loop[0],'|',loop[1],'REU')


	# Output to file
	with open('./output_files/best_loops.txt','w+') as f:
		for loop in loops_sorted[:num_loops]:
			line = loop[0] + '\t' + str(loop[1]) + '\n'
			f.write(line)

