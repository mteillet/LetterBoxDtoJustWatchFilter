# backend.py
from bs4 import BeautifulSoup
import requests
import re

def main():
    '''
    Main Function that will be replaced with frontend / gui call
    '''
    #letterBoxdListLink = 'https://letterboxd.com/mteillet/list/solo-watch-list/'
    #letterBoxdListLink = 'https://letterboxd.com/mteillet/list/need-to-watch/'
    letterBoxdListLink = 'https://boxd.it/jm3pY'
    # Getting the list
    filmList = getList(letterBoxdListLink)
    # Print only if you need to debug what's been found in the letterboxd parsing
    #logsLetterBoxData(filmList)
    # Comparing with justwatch database
    filmDict, servicesList = justwatchCompare(filmList)
    printInfosOnJustWatchList(filmDict, servicesList)

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
    #filmList = ["boyhood", "the-skin-i-live-in", "kairo", "fargo", "yi-yi", "possession", "kanikosen"]

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
            firstRow = soup.find("div", class_="title-list-row__row")
            #print(firstRow)
            if firstRow is not None:
                filmSoup = firstRow.find("a", class_="title-list-row__column-header")
            else:
                #print("None found for %s" % movie)
                filmSoup = None
            # print(filmSoup)
            #filmSoup = firstRow.find("article", class_="buybox")
            # Try except in case nothing exists no film is listed for this search
            try :
                spanTitle = filmSoup.find("span", class_="header-title")
                filmDict[movie]["jwTitle"] = spanTitle.text
            except AttributeError:
                filmDict[movie]["jwTitle"] = "NOT FOUND"
            
            # STREAMING SERVICES
            # Checking only first row in order to make sure if a service (stream or rent)
            # is missing, it does not return the results from the second row
            # Try except in case nothing exists no film is listed for this search
            try:
                filmSoup = firstRow.find("article", class_="buybox")
                streamSoup = filmSoup.find("div", class_="buybox-row stream inline")
            except AttributeError:
                streamSoup = None
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

    return(filmDict, servicesList)

def printInfosOnJustWatchList(filmDict, servicesList):
    for film in filmDict:
        if filmDict[film]["jwTitle"] == "NOT FOUND":
            print("\nERROR, couldn't find %s on just watch" % film)
        else:
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
                for rent in filmDict[film]["rent"]:
                    print(rent)

    print("\n\nThe following services were found while scanning the film list:")
    for service in servicesList:
        print(service)


if __name__ == "__main__":
    main()