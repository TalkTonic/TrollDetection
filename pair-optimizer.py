import numpy as np
from numpy import linalg as LA
from nltk.corpus import wordnet as wn

# generates a [(username, username), (username, username), ...] from a [(username, [interest, interest, ...]), (username, [interest, interest, ...]), ...]
def get_pairs_subgraph(user_interest_list):
	# calculate interest frequencies
	interest_frequencies = {}
	for user in user_interest_list:
		for interest in user[1]:
			try:
				interest_frequencies[interest] += 1
			except:
				interest_frequencies[interest] = 1

	# calculate the adjacency matrix
	A = np.zeros([len(user_interest_list), len(user_interest_list)])
	for i in range(0, len(user_interest_list)):
		for j in range(i, len(user_interest_list)):
			common_interests = set(user_interest_list[i][1]) & set(user_interest_list[j][1])
			# add weights of multiple common interests
			for interest in common_interests:
				# use interest frequencies as weights
				A[i][j] += interest_frequencies[interest]
				A[j][i] += interest_frequencies[interest]

	# calculate centrality vector as the all-positive eigenvector of A
	eigenvals, eigenvectors = LA.eig(A)
	eigenvectors_lists = eigenvectors.transpose().tolist()
	centrality_vector = []
	for vector in eigenvectors_lists:
		all_positive = True
		for element in vector:
			if element < 0:
				all_positive = False
		if all_positive:
			centrality_vector = vector
	
	# sort the users based on their centrality, map sorted indices to unsorted ones
	user_list_with_centrality = []
	for i in range(0, len(user_interest_list)):
		user_list.append(user_interest_list[i][0], centrality_vector[i], i)
	user_list_with_centrality = sorted(user_list, key = lambda x: x[1])

	# attempt to pair users, starting with least-central users
	pairings = []
	paired = set()
	for i in range(0, len(user_interest_list)):
		for j in range(i, len(user_interest_list)):
			if i in paired or j in paired:
				continue
			if set(user_interest_list[user_list_with_centrality[i][2]][1]) & set(user_interest_list[user_list_with_centrality[j][2]][1]):
				pairings.append((user_list_with_centrality[i][0], user_list_with_centrality[j][0]))
				paired.add(i)
				paired.add(j)

	# accumulate unpaired (leftover) users
	leftovers = []
	for i in range(0, len(user_interest_list)):
		if i not in paired:
			leftovers.append(user_list_with_centrality[i][0])

	# return pairings and leftovers
	return (pairings, leftovers)

# expands interests using wordnet, trying to pair leftovers until all thats left is to pair them randomly
def get_pairs_leftovers(user_interest_list):
	paired = set()
	pairings = []
	leftovers = []

	for i in range(0, 5):
		# expand interests to include interest synonyms
		for user in user_interest_list:
			for interest in user[1]:
				for synset in wn.synsets(interest):
					for lemma_name in synset.lemma_names()
						if lemma_name not in user[1]:
							user[1].append(lemma_name)
					for hyponym in synset.hyponyms()
						if hyponym not in user[1]:
							user[1].append(hyponym)
					for hypernym in synset.hypernyms()
						if hypernym not in user[1]:
							user[1].append(hypernym)
					for part_meronym in synset.part_meronyms()
						if part_meronym not in user[1]:
							user[1].append(part_meronym)
					for substance_meronym in synset.substance_meronyms()
						if substance_meronym not in user[1]:
							user[1].append(substance_meronym)
					for holonym in synset.holonyms()
						if holonym not in user[1]:
							user[1].append(holonym)
					for entailment in synset.entailments()
						if entailment not in user[1]:
							user[1].append(entailment)

		# generate new 

		# try getting pairs now
		temp_pairings, temp_leftovers = get_pairs_subgraph(user_interest_list)


def get_pairs(user_interest_list):
	# create a graph where users are nodes and edges are shared interests
	A = {}
	for i in range(0, len(user_interest_list)):
		A[i] = []
		for j in range(i, len(user_interest_list)):
			common_interests = set(user_interest_list[i][1]) & set(user_interest_list[j][1])
			if common_interests != set():
				A[i].append(j)
				A[j].append(i)

	# find all detatched graphs
	subgraph_node_list_list = []
	visited = set()
	fringe = []
	while True:
		# find an unvisited node - we will make a subgraph of all connected nodes
		done = True
		for node in A.keys():
			if node not in visited:
				fringe.append(node)
				done = False

		# if we did not find any unvisited nodes, our work here is done
		if done:
			break

		# perform a bfs to iteratively add all connected nodes to a subgraph node list
		subgraph_node_list = []
		while fringe:
			node = fringe.popleft()
			subgraph.append(node)
			for edge in A[node]:
				if edge not in visited:
					fringe.append(edge)

		# add that subgraph to our list of subgraph node lists
		subgraph_node_list_list.append(subgraph_node_list)

	# for each of the subgraph node lists, get the related user, interest tuples
	user_interest_tuple_list = []
	for subgraph_node_list in subgraph_node_list_list:
		sub_user_interest_list = []
		for user_tuple in user_interest_list:
			if user_tuple[0] in subgraph_node_list:
				sub_user_interest_list.append(user_tuple)
		user_interest_tuple_list.append(sub_user_interest_list)

	# compute the optimal pairings for subgraphs using helper functions
	pairings = []
	leftovers = []
	for sub_user_interest_list in user_interest_tuple_list:
		if len(sub_user_interest_list) == 1:
			leftovers = leftovers + sub_user_interest_list
		else:
			temp_pairings, temp_leftovers = get_pairs_subgraph(sub_user_interest_list)
			pairings.append(temp_pairings)
			leftovers = leftovers + temp_leftovers
	temp_pairings, temp_leftover = get_pairs_leftovers(leftovers)
	pairings.append(temp_pairings)

	# return the list of pairings and the leftover
	return (pairings, temp_leftover)

user_interest_list = [('a', ['1']), ('b', ['1']), ('c', ['1']), ('d', ['2'])]
print get_pairs(user_interest_list)