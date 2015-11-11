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

def process_tweet(text, afinnDict, word_score):
    words = preprocess(text)
    for word in words:
        if word in afinnDict:
            for otherWord in words:
                if (otherWord != word) and (otherWord not in afinnDict):
                    if otherWord not in word_score:
                        word_score[otherWord] = afinnDict[word]
                    else:
                        word_score[otherWord] += afinnDict[word] 
    return word_score

	
def main():
    word_score = {}
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    afinnDict = process_sent_file(sent_file)
    for line in tweet_file:
        tweet = json.loads(line)
        if 'text' in tweet:
            word_score = process_tweet(tweet['text'], afinnDict, word_score)
    for word, value in word_score.items():
        print word, value


if __name__ == '__main__':
    main()

