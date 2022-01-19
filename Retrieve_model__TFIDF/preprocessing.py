#########################
######## Imports ########
#########################

#import nltk
#nltk.download('punkt')
#nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer


#########################
##### Initialization ####
#########################

stemmer = SnowballStemmer(language='french')
stopWords = set(stopwords.words('french'))
tokenizer = RegexpTokenizer(r'\w+')


#########################
####### Functions #######
#########################

def tokenize(sentence):
    return tokenizer.tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def clean(sentence):
    clean_words = []
    for word in sentence:
        if word not in stopWords:
            clean_words.append(word)
    return clean_words
