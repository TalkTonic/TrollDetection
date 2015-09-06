import numpy as np
import nltk
from nltk import word_tokenize
from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()

target_words = ["u", "ur", "urself", "urselves", "y'", "ya", "ya'", "yall", "yas", "ye", "yeee", "yer", "yerself", "you", "youd", "your", "youre", "yours", "yourself", "yourselves", "youve"]
verb_parts = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

def targeted_sentiment(message):
        message = message.lower()
        # pre-process the message into multiple clauses (approximately)
        message_tokens = word_tokenize(message)
        tagged_tokens = nltk.pos_tag(message_tokens)
        message_clauses = []
        end_token_of_previous_clause = 0
        did_split = False
        for i in range(0, len(tagged_tokens)):
                # if there's a coordinating conjunction, 
                if tagged_tokens[i][1] == "CC":
                        # try to find an occurance of a target word and verb on each side of the conjunction
                        target_before = False
                        verb_before = False
                        target_after = False
                        verb_after = False
                        for j in range(end_token_of_previous_clause, i):
                                if tagged_tokens[j][0] in target_words:
                                        target_before = True
                                if tagged_tokens[j][1] in verb_parts:
                                        verb_before = True
                        if not target_before or not verb_before:
                                continue
                        for j in range(i + 1, len(message_tokens)):
                                if tagged_tokens[j][0] in target_words:
                                        target_after = True
                                if tagged_tokens[j][1] in verb_parts:
                                        verb_after = True
                        if not target_after or not verb_after:
                                continue
                        # if we did find those things, we need to split the message (and keep going on the second half)
                        temp = []
                        for j in range(end_token_of_previous_clause, i):
                                temp.append(message_tokens[j])
                        message_clauses.append(temp)
                        temp = []
                        for j in range(i + 1, len(message_tokens)):
                                temp.append(message_tokens[j])
                        message_clauses.append(temp)
                        end_token_of_previous_clause = i + 1
                        did_split = True
        if not did_split:
                message_clauses.append(message_tokens)

        # get a list of the sentiments associated with all target words
        sentiment_list = []
        for this_clause in message_clauses:
                for target in target_words:
                        if target in this_clause:
                                text = ""
                                for token in this_clause:
                                        text += token
                                        text += " "
                                alchemyapi_result = alchemyapi.sentiment_targeted("text", text, target)
                                if alchemyapi_result["docSentiment"]["type"] != "neutral":
                                        try:
                                                sentiment_list.append(float(alchemyapi_result["docSentiment"]["score"]))
                                        except:
                                                print "ALCHEMY API PROBLEM! <troll-detector.py>", alchemyapi_result
                                else:
                                        sentiment_list.append(float(0))
        if len(sentiment_list) == 0:
                
                try:
                        return [(.8)*float(alchemyapi.sentiment("text",message)['docSentiment']['score'])]
                except:
                        return [0]

        # return the list of results of all the sentiment queries
        return sentiment_list

if __name__ == '__main__':
        while True:
                message = raw_input("Enter a message: ")
                result = targeted_sentiment(message)
                mean = sum(result)/len(result)

                print "results:\t", result
                print "mean:\t", mean
                print ""
