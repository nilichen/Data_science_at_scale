import sys
import json
import re

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

def process_tweet(text, afinnDict):
    words = preprocess(text)
    return sum([afinnDict[word] if word in afinnDict else 0 for word in words])

	
def main():
    tweets_score = {}
    i = 0
    sent_file = open('AFINN-111.txt')
    tweet_file = open('output.json')
    afinnDict = process_sent_file(sent_file)
    for line in tweet_file:
        i += 1
        tweet = json.loads(line)
        if 'text' in tweet:
            tweets_score[i] = process_tweet(tweet['text'], afinnDict)
        else:
            tweets_score[i] = 0
    for value in tweets_score.values():
        print value

if __name__ == '__main__':
    main()
