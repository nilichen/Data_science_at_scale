# -*- coding: utf-8 -*-
import sys
import json
import re
import operator

def process_sent_file(afinnfile):
	scores = {} 
	for line in afinnfile:
         term, score  = line.split("\t")
         scores[term] = int(score)  
	return scores
 

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def process_tweet(text, location, afinnDict, state_score):
    words = preprocess(text)
    if location:
        if location not in state_score:
            state_score[location] = sum([afinnDict[word] if word in afinnDict else 0 for word in words])
        else:
            state_score[location] += sum([afinnDict[word] if word in afinnDict else 0 for word in words])

    return state_score
	
def main():
    state_score = {}
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    afinnDict = process_sent_file(sent_file)
    for line in tweet_file:
        tweet = json.loads(line)
        if ('text' in tweet) and ('place' in tweet) and tweet['place'] != None:
            if ('country_code' in tweet['place']):
                state_score = process_tweet(tweet['text'], tweet['place']['country_code'], afinnDict, state_score)

    print max(state_score.iteritems(), key=operator.itemgetter(1))[0]

if __name__ == '__main__':
    main()

