# letterBoxDtoJwFilter_cli.py
from backend import getList, justwatchCompare

def main():
    # Get link
    link = getLetterBoxDLink()
    #print("Link is : \n%s" % link)
    lbdList = getList(link)
    filmDict, servicesList = justwatchCompare(lbdList)
    streamOrRent = getUserStreamOrRentWish()
    servicesList.sort()
    userServices = getUserServices(servicesList)
    filmDictVsServices(filmDict, servicesList, userServices, streamOrRent)

def getLetterBoxDLink():
    '''
    Getting a letter box d list link from the user
    '''
    return input("Paster a LetterBoxD list link :\n")

def getUserStreamOrRentWish():
    '''
    Asks the user if he wants to stream, rent or both
    '''
    print("\nDo you want to stream or rent movies ?")
    return input("0 - Stream\n1 - Rent\n3 - Both\n")


def getUserServices(servicesList):
    '''
    Getting the user to input the list of services he is suscribed to
    Returns it as a list of indexes to be used with the servicesList
    '''
    print("\nSelect the services you have at your disposal :\n(Use the number and a comma between each number)")
    current = 0
    for service in servicesList:
        print("%i - %s" % (current, service))
        current += 1

    userServices = input("Services Number list : \n")
    userServices = userServices.split(",")

    print("\nYou have selected :")
    for i in userServices:
        print(servicesList[int(i)])
    return(userServices)

def filmDictVsServices(filmDict, servicesList, userServices, streamOrRent):
    '''
    Comparing services with the film dict to show the user what he can actually watch
    '''
    streamingDict = {}
    rentingDict = {}

    for i in userServices:
        # Streaming
        if streamOrRent != "1":
            streamingDict[servicesList[int(i)]] = []
            for film in filmDict:
                if servicesList[int(i)] in filmDict[film]["streaming"]:
                    streamingDict[servicesList[int(i)]].append(filmDict[film]["jwTitle"])

        # Renting
        if streamOrRent != "0":
            rentingDict[servicesList[int(i)]] = []
            for film in filmDict:
                if servicesList[int(i)] in filmDict[film]["rent"]:
                    rentingDict[servicesList[int(i)]].append(filmDict[film]["jwTitle"])

    # Results for user
    if streamOrRent != 1:
        print(("\n\nAvailable for streaming :").upper())
        for service in streamingDict:
            if streamingDict[service]:
                print("\n%s streaming :" % service)
                for movie in streamingDict[service]:
                    print("- %s" % movie)
            else:
                #print("\n%s streaming :\n- None" % service)
                pass

    if streamOrRent != 0:
        print(("\n\nAvailable for renting:").upper())
        for service in rentingDict:
            if rentingDict[service]:
                print("\n%s renting:" % service)
                for movie in rentingDict[service]:
                    print("- %s" % movie)
            else:
                #print("\n%s renting :\n- None" % service)
                pass
    

if __name__ == "__main__":
    main()