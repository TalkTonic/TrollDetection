import numpy as np
from numpy import linalg as LA
from nltk.corpus import wordnet as wn
from collections import deque

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
		for j in range(i + 1, len(user_interest_list)):
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
		all_negative = True
		for element in vector:
			if element < 0:
				all_positive = False
			if element > 0:
				all_negative = False
		if all_positive or all_negative:
			centrality_vector = vector
	
	# sort the users based on their centrality, map sorted indices to unsorted ones
	user_list_with_centrality = []
	for i in range(0, len(user_interest_list)):
		user_list_with_centrality.append((user_interest_list[i][0], centrality_vector[i], i))
	user_list_with_centrality = sorted(user_list_with_centrality, key = lambda x: x[1])

	# attempt to pair users, starting with least-central users
	pairings = []
	paired = set()
	for i in range(0, len(user_interest_list)):
		for j in range(i + 1, len(user_interest_list)):
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

	for i in range(0, 1):
		if len(user_interest_list) == len(paired):
			break
		# expand interests to include related words of all form (except antonyms)
		for user in user_interest_list:
			temp_interests = list(user[1])
			for interest in user[1]:
				for synset in wn.synsets(interest):
					for lemma_name in synset.lemma_names():
						if lemma_name not in temp_interests and lemma_name not in user[1]:
							temp_interests.append(lemma_name)
			user = (user[0], temp_interests)

		# generate new user_interest_list from thus-unpaired users
		sub_user_interest_list = []
		for i in range(0, len(user_interest_list)):
			if user_interest_list[i][0] not in paired:
				sub_user_interest_list.append(user_interest_list[i])

		# try getting pairs now
		temp_pairings, temp_leftovers = get_pairs_subgraph(sub_user_interest_list)
		for pair in temp_pairings:
			paired.add(pair[0])
			paired.add(pair[1])

	# pair extraneous leftovers
	for i in range(0, len(user_interest_list)):
		for j in range(i + 1, len(user_interest_list)):
			if user_interest_list[i][0] not in paired and user_interest_list[j][0] not in paired:
				pairings.append((user_interest_list[i][0], user_interest_list[j][0]))
				paired.add(user_interest_list[i][0])
				paired.add(user_interest_list[j][0])

	# the leftover is the only one not to be paired
	leftover = None
	for user in user_interest_list:
		if user[0] not in paired:
			leftover = user[0]

	# return the pairings and leftover
	return (pairings, leftover)

def get_pairs(user_interest_list):
	# create a graph where users are nodes and edges are shared interests
	A = {}
	for i in range(0, len(user_interest_list)):
		A[user_interest_list[i][0]] = []
	for i in range(0, len(user_interest_list)):
		for j in range(i, len(user_interest_list)):
			common_interests = set(user_interest_list[i][1]) & set(user_interest_list[j][1])
			if common_interests != set():
				if j not in A[user_interest_list[i][0]]:
					A[user_interest_list[i][0]].append(user_interest_list[j][0])
				if i not in A[user_interest_list[j][0]]:
					A[user_interest_list[j][0]].append(user_interest_list[i][0])

	# remove self-references (not sure why I had to do this twice...)
	for key in A.keys():
		A[key].remove(key)
		A[key].remove(key)

	# find all detatched graphs
	subgraph_node_list_list = []
	visited = set()
	fringe = deque([])
	while True:
		# find an unvisited node - we will make a subgraph of all connected nodes
		done = True
		for node in A.keys():
			if node not in visited:
				fringe.append(node)
				visited.add(node)
				done = False
				break

		# if we did not find any unvisited nodes, our work here is done
		if done:
			break

		# perform a bfs to iteratively add all connected nodes to a subgraph node list
		subgraph_node_list = []
		while fringe:
			node = fringe.popleft()
			subgraph_node_list.append(node)
			for edge in A[node]:
				if edge not in visited:
					fringe.append(edge)
					visited.add(edge)

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
		elif len(sub_user_interest_list) > 1:
			temp_pairings, temp_leftovers = get_pairs_subgraph(sub_user_interest_list)
			pairings = pairings + temp_pairings
			temp_leftover_tuples = []
			for user in user_interest_list:
				for temp_leftover in temp_leftovers:
					if user[0] == temp_leftover:
						temp_leftover_tuples.append(user)
			leftovers = leftovers + temp_leftover_tuples
	temp_pairings, temp_leftover = get_pairs_leftovers(leftovers)
	pairings = pairings + temp_pairings

	# return the list of pairings and the leftover
	return (pairings, temp_leftover)

user_interest_list = [('adam', ['code', 'eat', 'walk']), ('barbara', ['code', 'sleep']), ('chris', ['sleep', 'eat']), ('debra', ['slumber', 'eat']), ('ernest', ['eat', 'code', 'walk']), ('farah', ['slumber']), ('herman', ['slumber'])]
print get_pairs(user_interest_list)