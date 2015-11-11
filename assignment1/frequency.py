# -*- coding: utf-8 -*-
import sys
import json
import re

 

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

def process_tweet(text, word_frequency):
    words = preprocess(text)
    for word in words:
        if word not in word_frequency:
            word_frequency[word] = 1
        else:
            word_frequency[word] += 1 
    return word_frequency

	
def main():
    word_frequency = {}
    tweet_file = open(sys.argv[1])
    for line in tweet_file:
        tweet = json.loads(line)
        if 'text' in tweet:
            word_frequency = process_tweet(tweet['text'], word_frequency)
    total = sum(word_frequency.values())
    for word, value in word_frequency.items():
        print word, value/float(total)


if __name__ == '__main__':
    main()
