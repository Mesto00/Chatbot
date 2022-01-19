#### IMPORT ####

import json

from corpus_tfidf import tf_idf_compute

from title_detection import identify_title, read_result

#### CODE ####

with open("corpus_questions.json", "r", encoding="utf-8") as file:
    json_file = json.loads(file.read())
    
content = json_file['intents']

corpus_temp = []
corpus = []
for i in range(len(content)):
    corpus_temp.append(content[i]['examples'])
    for j in range(len(corpus_temp[i])):
        corpus.append(corpus_temp[i][j])
        
''''''

introduction = "\nBonjour, je suis Alex, votre chatbot AlloCine.\n" + \
    "Je peux répondre à toutes vos questions sur de nombreux films : " + \
    "le réalisateur, le genre, la durée, la note des spectateurs, le synopsis etc ... \n"
print(introduction)

# Title of the film 

while True:
    
    filmAsked = input("Tout d'abord, pourriez-vous rentrer le film sur lequel vous souhaitez des informations : ")
    
    filmTitles, filmIndexes = identify_title(filmAsked)
    
    print('\nLe film choisi est-il l\'un des trois ci-dessous ?')
    print(filmTitles)
    inList = input('Si oui, indiquez son numéro dans la liste, si non écrivez "erreur" : ')
    
    errorMessage = "\nApparemment, vous n'avez pas trouvé votre film dans la liste, nous allons donc recommencer"
    
    try:
        if int(inList) in [1, 2, 3]:
            numFilm = filmIndexes[int(inList) - 1]
            break
        print(errorMessage)
    except:
        print(errorMessage)


# Questions sur le film

while True:
    
    questionAsked = input('Quelle est votre question ? : ')
    corpus.append(questionAsked)
    
    index, cos_similarity = tf_idf_compute(corpus)
    
    intent = -1
    count = -1
    
    while (count < index):
        intent += 1
        count += len(content[intent]['examples'])
    
    nameClass = content[intent]['intent']
    
    if nameClass == "goodbye":
        print("Au revoir et à bientôt j'espère !")
        break
    
    result = read_result(numFilm, nameClass)
    
    print(result)
    
    del corpus[-1]
