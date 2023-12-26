# backend.py
from bs4 import BeautifulSoup
import requests
import re

def main():
    '''
    Main Function that will be replaced with frontend / gui call
    '''
    letterBoxdListLink = 'https://letterboxd.com/mteillet/list/solo-watch-list/'
    # Getting the list
    filmList = getList(letterBoxdListLink)
    # Print only if you need to debug what's been found in the letterboxd parsing
    logsLetterBoxData(filmList)
    # Comparing with justwatch database
    justwatchCompare(filmList)

def getList(listLink):
    '''
    Get the contents from a letterBoxd list and returns it
    '''
    listPage = requests.get(listLink)

    # Check there was no error getting the list 
    if listPage.status_code != 200:
        return print("ERROR LOADING THE LINK")

    soup = BeautifulSoup(listPage.content ,features="html.parser")
    filmSoup = (soup.find_all("li", class_="poster-container"))
    filmList = []
    for film in filmSoup:
        #print(film)
        posterContainer = film.find("div", class_="really-lazy-load")
        #print(posterContainer.find("div", class_="data-film-slug"))
        regex = re.compile('data-film-slug=["\'](.*?)["\']')
        movieName = regex.search(str(posterContainer)).group(1)
        filmList.append(movieName)

    return filmList

def logsLetterBoxData(filmList):
    '''
    Inspects the contents found on the letterboxd film lists, returns the move names and the number of films
    '''
    print("Here is the films founds :")
    for film in filmList:
        print(film)
    
    print("\nFound %i films in the LetterBoxD list" % (len(filmList)))

def justwatchCompare(filmList):
    '''
    Checks the availibility of the movies with justwatch database
    '''
    justWatchURL = 'https://www.justwatch.com/fr'
    
    # Temp test on single movie
    filmList = ["the-skin-i-live-in"]

    # TODO !!!
    # Need to test searching on justwatch directly

    for movie in filmList:
        # Get the letterboxd film page
        justWatchLink = "%s/recherche?q=%s" % (justWatchURL, movie.replace("-", " "))
        justWatchSearch = requests.get(justWatchLink)

        # Check there was no error getting the list 
        if justWatchSearch.status_code != 200:
            return print("ERROR LOADING THE LINK")
        
        soup = BeautifulSoup(justWatchSearch.content, features="html.parser")
        filmSoup = soup.find_all("div", class_="title-list-row__column")
        spanTitle = filmSoup[1].find("span", class_="header-title")
        print(spanTitle.text)

        '''
        for span in spans:
            # if span.text == "The Skin I Live In":
            print(span)
        '''
        #title = filmSoup.find("span", class_="header-title")
        #print(title)


if __name__ == "__main__":
    main()