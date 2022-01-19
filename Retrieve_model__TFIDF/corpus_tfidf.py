#########################
######## Imports ########
#########################

import pandas as pd

from scipy import linalg, mat, dot

from preprocessing import tokenize, stem, clean

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer  


#########################
#### Initializisation ###
#########################

vectorizer = CountVectorizer()

#########################
######### CODE ##########
#########################

def tf_idf_compute(corpus):
    
    ''' Step 1 = Preprocessing '''
    
    new_sentences = []
    
    for index, sentence in enumerate(corpus):
        new_sentence = tokenize(sentence)
        new_sentence = clean(new_sentence)
        for idx, word in enumerate(new_sentence):
            new_sentence[idx] = stem(word)
        new_sentence = " ".join(new_sentence)
        new_sentences.append(new_sentence)
    
    
    ''' Step 2 = TF-IDF matrix building '''
        
    tfidf_vectorizer = TfidfVectorizer(use_idf=True) 
    tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(new_sentences)
    
    df = pd.DataFrame(columns=tfidf_vectorizer.get_feature_names())
    
    for i in range(len(corpus)):
        
        vector_tfidfvectorizer = tfidf_vectorizer_vectors[i] 
        matrix = vector_tfidfvectorizer.T.todense()
        
        # Place tf-idf values in a pandas data frame 
        dfNew = pd.DataFrame(matrix, index=tfidf_vectorizer.get_feature_names())
        df = df.append(dfNew.T, ignore_index=True)
        
        
    ''' Step 3 = Cos-similarity computation '''
    
    cos_similarity = []
    
    df_list = df.values.tolist()
    
    a = mat(df_list[-1])
    
    for i in range(len(corpus) - 1):
    
        b = mat(df_list[i])
        c = dot(a,b.T)/linalg.norm(a)/linalg.norm(b)
        
        cos_similarity.append(c)
        
    max_ind = cos_similarity.index(max(cos_similarity))
    
    return max_ind, cos_similarity




