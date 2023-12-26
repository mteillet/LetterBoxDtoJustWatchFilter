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
    #logsLetterBoxData(filmList)
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
    #filmList = ["boyhood", "the-skin-i-live-in", "kairo", "fargo"]

    filmDict = {}
    servicesList = []

    current = 1
    for movie in filmList:
        print("Scanning %i / %i, ---> %s" % (current, len(filmList), movie))
        filmDict[movie] = {}
        # Get the letterboxd film page
        justWatchLink = "%s/recherche?q=%s" % (justWatchURL, movie.replace("-", " "))
        justWatchSearch = requests.get(justWatchLink)

        # Check there was no error getting the list 
        if justWatchSearch.status_code != 200:
            filmDict[movie]["Error"] = True
        else:
            filmDict[movie]["Error"] = False
        
            soup = BeautifulSoup(justWatchSearch.content, features="html.parser")
            filmSoup = soup.find_all("div", class_="title-list-row__column")
            try :
                spanTitle = filmSoup[1].find("span", class_="header-title")
                filmDict[movie]["jwTitle"] = spanTitle.text
            except IndexError:
                filmDict[movie]["jwTitle"] = "NOT FOUND"
            
            # STREAMING SERVICES
            streamSoup = soup.find("div", class_="buybox-row stream inline")
            # In case ne streaming service is available
            if streamSoup is None:
                imgs = ['alt="None"']
            else:
                imgs = streamSoup.find_all("img")
            #print(streamSoup)
            filmDict[movie]["streaming"] = []
            for img in imgs:
                #print(img)
                regex = re.compile('alt=["\'](.*?)["\']')
                streamingService = regex.search(str(img)).group(1)
                filmDict[movie]["streaming"].append(streamingService)
                if streamingService not in servicesList:
                    servicesList.append(streamingService)

            # RENTING SERVICES
            rentSoup = soup.find("div", class_="buybox-row rent inline")
            if rentSoup is None:
                imgs = ['alt="None"']
            else:
                imgs = rentSoup.find_all("img")
            filmDict[movie]["rent"] = []
            for img in imgs:
                #print(img)
                regex = re.compile('alt=["\'](.*?)["\']')
                rentingService = regex.search(str(img)).group(1)
                filmDict[movie]["rent"].append(rentingService)
                if rentingService not in servicesList:
                    servicesList.append(rentingService)

        current += 1

    for film in filmDict:
        print("\n%s on JustWatch" % filmDict[film]["jwTitle"])
        if filmDict[film]["streaming"][0] == "None":
            print("Can't be streamed")
        else:
            print("Can be streamed on :")
            for stream in filmDict[film]["streaming"]:
                print(stream)
        if filmDict[film]["rent"][0] == "None":
            print("Can't be rented")
        else:
            print("Can be rented on :")
            for rent in filmDict[movie]["rent"]:
                print(rent)

    print("\n\nThe following services were found while scanning the film list:")
    for service in servicesList:
        print(service)


if __name__ == "__main__":
    main()