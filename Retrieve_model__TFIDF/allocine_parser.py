#########################
######## Imports ########
#########################

import pandas as pd
import requests
from lxml import html


#########################
#### Initializisation ###
#########################

data = []
count = 1
pages_parsed = 30

def clean(text):
    return text.replace('\n', '').strip()

def extractInfo(rawExtraction, value):
    if value in rawExtraction:
        index = rawExtraction.index(value)
        return clean(rawExtraction[index + 1])
    else:
        return '-'
    


#########################
######### CODE ##########
#########################


## Loop until the number of pages to parse is reached
while count <= pages_parsed:
    
    front_page = "https://www.allocine.fr/film/meilleurs/?page=" + str(count)
    response = requests.get(front_page)
    extractedHtml = html.fromstring(response.content)
    # Extract the URLS of the films on the page
    urls = extractedHtml.xpath('.//div[@class="gd-col-middle"]/ol/li/div/div/h2/a/@href')
    count += 1 
    
    # Go on each webpage gathered at the previous step
    
    for url in urls:

        url = 'https://www.allocine.fr' + url
        film_page = requests.get(url)
        filmHtml = html.fromstring(film_page.content)
        
        # Get the title of the film
        title_info = filmHtml.xpath('.//div[contains(@class, "titlebar-page")]/div/text()')
        title = clean(title_info[0])
        
        # Get the date of release and the type of film
        general_info = filmHtml.xpath('.//div[contains(@class, "meta-body-info")]/span/text()')
        date = clean(general_info[0])
        genre = ", ".join(general_info[3:])
        
        # Get the lengh of the movie
        duree = filmHtml.xpath('.//div[contains(@class, "meta-body-info")]/text()')
        duree = clean(duree[3])
        
        # Get the director and the main actors
        director = filmHtml.xpath('.//div[contains(@class, "meta-body-direction")]/span/text()')[1:]
        director = ", ".join(director)
        actors = filmHtml.xpath('.//div[contains(@class, "meta-body-actor")]/span/text()')[1:]
        actors = ", ".join(actors)
        
        # Get the nationality
        nationality = filmHtml.xpath('.//div[@class="meta-body-item"]/span/text()')
        nationality = clean(nationality[-1])
        
        # Get the ratings
        
        essai = filmHtml.xpath('.//div[contains(@class, "rating-item-content")]/span/text()')
        if len(essai) == 2:
            ratings = filmHtml.xpath('.//div[contains(@class, "stareval stareval-medium")]/span[1]/text()')
            pressRating = float(clean(ratings[0]).replace(',','.'))
            peopleRating = float(clean(ratings[1]).replace(',','.'))
                                 
            numberRatings = filmHtml.xpath('.//div[contains(@class, "stareval stareval-medium")]/span[2]/text()')
            pressNumber = clean(numberRatings[0])
            peopleNumber = clean(numberRatings[1])
        elif len(essai) == 1:
            ratings = filmHtml.xpath('.//div[contains(@class, "stareval stareval-medium")]/span[1]/text()')
            peopleRating = float(clean(ratings[0]).replace(',','.'))
                                 
            numberRatings = filmHtml.xpath('.//div[contains(@class, "stareval stareval-medium")]/span[2]/text()')
            peopleNumber = clean(numberRatings[0])
            pressRating, pressNumber = '-', '-'
        else:
            peopleRating, peopleNumber, pressRating, pressNumber = '-', '-', '-', '-'
            
        
        # Get the synopsis
        rawSynopsis = filmHtml.xpath('.//section[@id="synopsis-details"]/div[contains(@class, "content-txt")]/text()')
        synopsis = ''
        for elt in rawSynopsis:
            synopsis += clean(elt)
            
        if not synopsis:
            rawSynopsis = filmHtml.xpath('.//section[@id="synopsis-details"]/div[contains(@class, "content-txt")]/p/text()')
        synopsis = ''
        for elt in rawSynopsis:
            synopsis += clean(elt)
            
        
        # Get the "distributeur" and awards
        moreInfo = filmHtml.xpath('.//div[@class="ovw-synopsis-info"]/div/span/text()')
        
        for elt in moreInfo:
            elt = clean(elt)
        
        distributeur = extractInfo(moreInfo, 'Distributeur')
        awards = extractInfo(moreInfo, 'Récompenses')
        
        hiddenInfo = filmHtml.xpath('.//div[@class="more-hidden"]/div/span/text()')
        
        # Cleaning the hidden info
        for elt in hiddenInfo:
            elt = clean(elt)
            
        entries = ['Date de sortie DVD', 'Box Office France', 'Budget', 'N° de Visa']
        
        dateDVD = extractInfo(hiddenInfo, entries[0])
        BoxOffice = extractInfo(hiddenInfo, entries[1])
        budget = extractInfo(hiddenInfo, entries[2])
        numVisa = extractInfo(hiddenInfo, entries[3])
  
        # Put the results in the list
        data.append([title, date, genre, duree, director, actors, nationality, synopsis, distributeur, awards, dateDVD, BoxOffice, budget, numVisa, pressRating, peopleRating, pressNumber, peopleNumber, url])

# Turn the list into a dataframe
columns = ['titre', 'date', 'genre', 'duree', 'realisateur', 'acteurs', 'nationalite', 'synopsis', 'distributeur', 'recompenses', 'date_sortie_dvd', 'box_office', 'budget', 'visa', 'note_presse', 'note_spectateurs', 'nombre_presse', 'nombre_spectateurs', 'url']
df = pd.DataFrame(data=data, columns=columns)
# Create the csv file
df.to_csv('allocine_parser_results.csv', sep=';', index=False)
