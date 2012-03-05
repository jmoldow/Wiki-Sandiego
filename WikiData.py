import json
import shelve 

'''
Provides methods for easily manipuating data from Wikipedia.
Uses the API at http://en.wikipedia.org/w/api.php.
'''
class WikiData:
    
    '''
    Initializes the WikiData class
    '''
    def __init__(name='wikicache'):
        self.limit=500
        self.format='json'
        self.name=name
        self.initializeDB(self.name)
    
    '''
    Initializes the database. Creates the database file if needed, and loads it into the instance of the class.
    @param name The name of the desired database to check/create
    @return boolean Returns true if the database needed to be created.
    '''
    def initializeDB(name):
#        wikicache['WhereInWiki'] = SetOfAllCountries (or whatever we are using as the possible starting points)
#        wikicache[articleName] = { 'forward':forwardLinksStringSet, 'backward':backwardLinkStringSet }
        pass
    
    '''
    Queries the database for a specific entry, adding it if need be.
    @param query A string to query in the database
    '''
    def queryDB(query):
        if query=='WhereInWiki':
            pass
        else:
            pass
    
    '''
    Saves the database to a local file.
    @param name The name of the desired database to save
    @return boolean Returns true if the database saved properly
    '''
    def saveDB(name):
        pass
    
    '''
    Gets the set of all countries and adds them to the database for future use.
    '''
    def getAllCountries():
        countries = set([])
        countries.update(getCategoryMembers('Category:Northern_American_countries'))
        countries.update(getCategoryMembers('Category:Central_American_countries'))
        countries.update(getCategoryMembers('Category:South_American_countries'))
        countries.update(getCategoryMembers('Category:European_countries'))
        countries.update(getCategoryMembers('Category:Southeast_Asian_countries'))
        countries.update(getCategoryMembers('Category:East_Asian_countries'))
        countries.update(getCategoryMembers('Category:African_countries'))
        countries.update(getCategoryMembers('Category:Middle_Eastern_countries'))
        countries.update(getCategoryMembers('Category:Western_Asian_countries'))
        countries.update(getCategoryMembers('Category:South_Asian_countries'))
        countries.update(getCategoryMembers('Category:Near_Eastern_countries'))
        
        #Get rid of the following articles, not actually countries:
        countries.discard('List of sovereign states and dependent territories in Africa')
        countries.discard('Flags of Africa')
        countries.discard('List of African countries by Human Development Index')
        countries.discard('List of African countries by population density')
        countries.discard('List of sovereign states and dependent territories in South America')
        countries.discard('List of sovereign states and dependent territories in Europe')
        countries.discard('European microstates')
        
        pass
    
    '''
    Returns a set of all articles that are linked from a given article.
    @param article The name of the article (with or without whitespace)
    '''
    def getArticleForwardLinks(article):
        urlText = 'http://en.wikipedia.org/w/api.php?action=query&prop=links&'+article+'&pllimit='+limit+'&format='+format
        pass
    
    '''
    Returns a set of all articles that linked to a given article.
    @param article The name of the article (with or without whitespace)
    '''
    def getAricleBacklinks(article):
        urlText = 'http://en.wikipedia.org/w/api.php?action=query&list=backlinks&'+article+'&bllimit='+limit+'&format='+format
        pass
    
    '''
    Returns a set of all pages in a particular category
    @param article The name of the article (with or without whitespace)
    '''
    def getCategoryMembers(article, type='page'):
        urlText = 'http://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle='+article+'&cmtype='+type+'&cmlimit='+limit
        pass
       
    def chooseClues(article, num=8):
        pass
    