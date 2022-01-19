#########################
######## Imports ########
#########################

import pandas as pd

from scipy import linalg, mat, dot

from preprocessing import tokenize, stem

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer  


#########################
#### Initializisation ###
#########################

vectorizer = CountVectorizer()

metadata = pd.read_csv('allocine_parser_results.csv', sep=';')
data_titles = metadata['titre']



#########################
######### CODE ##########
#########################

def identify_title(filmAsked):

    titles = pd.concat([data_titles, pd.Series([filmAsked])], ignore_index = True)
    n = len(titles)
    
    ''' Step 1 = Preprocessing without StopWords '''
    
    new_titles = []
    
    for index, title in titles.iteritems():
        new_title = tokenize(title)
        for idx, word in enumerate(new_title):
            new_title[idx] = stem(word)
        new_title = " ".join(new_title)
        new_titles.append(new_title)
        
    
    ''' Step 2 = TF-IDF matrix building '''
        
    tfidf_vectorizer = TfidfVectorizer(use_idf=True)
    tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(new_titles)
    
    tfidf_matrix = pd.DataFrame(columns=tfidf_vectorizer.get_feature_names())
    
    for i in range(n):
        
        vector_tfidfvectorizer = tfidf_vectorizer_vectors[i] 
        row = vector_tfidfvectorizer.T.todense()
        
        # Place tf-idf values in a pandas data frame 
        dfNew = pd.DataFrame(row, index=tfidf_vectorizer.get_feature_names())
        tfidf_matrix = tfidf_matrix.append(dfNew.T, ignore_index=True)
        
    
    ''' Step 3 = Cos-similarity computation '''
    
    cos_similarity = []
    
    tfidf_list = tfidf_matrix.values.tolist()
    
    a = mat(tfidf_list[-1])
    
    for i in range(n-1):
    
        b = mat(tfidf_list[i])
        c = (dot(a,b.T)/linalg.norm(a)/linalg.norm(b)).item()
        
        cos_similarity.append(c)
    
    
    similarities = pd.Series(cos_similarity)
    similarities = similarities.sort_values()
    indexes = similarities[-3:].index.tolist()
    indexes.reverse()
    
    expectedFilms = []
    
    for index in indexes:
        expectedFilms.append(titles[index])
        
    return expectedFilms, indexes


def read_result(index, nameClass):
    
    return metadata[nameClass][index]

    

