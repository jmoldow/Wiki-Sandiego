import json
import shelve
import string
import urllib

DEBUG=True

'''
Provides methods for easily manipuating data from Wikipedia.
Uses the API at http://en.wikipedia.org/w/api.php.
'''
class WikiData:
    '''
    Initializes the WikiData class
    '''
    def __init__(self, name='wikiCache'):
        self.initializeDB(name)
        
    '''
    Initializes the database. Creates the database file if needed, and loads it into the instance of the class.
    *Private
    @param name The name of the desired database to check/create
    @return boolean Returns true if the database needed to be created.
    NEED - error handling
    '''
    def initializeDB(self, name):
        self.wikiCache = shelve.open(name)
        if self.wikiCache.get('WhereInWiki',None)==None:
            self.wikiCache['WhereInWiki'] = self.getAllCountries()
            self.wikiCache.sync()

    '''
    Queries the database for a specific entry, adding it if need be.
    *Public
    @param query A article to query in the database
    NEED - error handling
    '''
    def queryDB(self, query):
        query = query.encode('utf-8')
        if query=='WhereInWiki' and self.wikiCache.get('WhereInWiki',None)==None:
            self.wikiCache['WhereInWiki'] = self.getAllCountries()
        elif str(query) not in self.wikiCache:
            self.wikiCache[str(query)] = {
                'forward':self.getArticleLinks(query,'forward'),
                'backward':self.getArticleLinks(query,'backward'),
                'images':self.getArticleLinks(query,'images'),
                'categories': self.getArticleLinks(query,'categories')
                }
        return self.wikiCache.get(str(query),None)
    
    '''
    Closes the class, properly storing the cache.
    *Public
    '''
    def close(self):
        self.wikiCache.close()
    
    '''
    Gets the set of all countries and adds them to the database for future use.
    *Private
    '''
    @staticmethod
    def getAllCountries():
        countries = set([])
        countries.update( WikiData.getArticleLinks('Category:Northern_American_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:Central_American_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:South_American_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:European_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:Southeast_Asian_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:East_Asian_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:African_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:Middle_Eastern_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:Western_Asian_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:South_Asian_countries','pages') )
        countries.update( WikiData.getArticleLinks('Category:Near_Eastern_countries','pages') )
        #Get rid of the following articles, not actually countries:
        countries.discard('List of sovereign states and dependent territories in Africa')
        countries.discard('Flags of Africa')
        countries.discard('List of African countries by Human Development Index')
        countries.discard('List of African countries by population density')
        countries.discard('List of sovereign states and dependent territories in South America')
        countries.discard('List of sovereign states and dependent territories in Europe')
        countries.discard('European microstates')
        countries.discard('List of Middle East countries by population')
        return countries
    
    
    '''
    Returns a the requested query type on the given article.
    *Private
    @param type the type of links that you want ('forward', 'backward', 'images', 'pages', 'categories')
    @param article The name of the article (with or without whitespace)
    @param cont the entire string nested in query continue(None by default)
    @return a list of all of the desired links
    NEED error handling, continuation
    '''
    @staticmethod
    def getArticleLinks(article, type, cont=None, limit='500', format='json'):
#        article = article.encode('ascii')
        urlTemplate = string.Template('http://en.wikipedia.org/w/api.php?action=query$t$a$l$f$c$o') #$t=type, $a = article, $l = limit, $f=format, $c=continue, $o=other
        if type=='forward':
            ns = 0
            if cont==None: urlName = urlTemplate.substitute(
                t='&prop=links',
                a='&titles='+article,
                l='&pllimit='+limit,
                f='&format='+format,
                c='',
                o='')
            else: urlName = urlTemplate.substitute(
                t='&prop=links',
                a='&titles='+article,
                l='&pllimit='+limit,
                f='&format='+format,
                c='&plcontinue='+cont,
                o='')
        if type=='backward':
            ns = 0
            if cont==None: urlName = urlTemplate.substitute(
                t='&list=backlinks',
                a='&bltitle='+article,
                l='&bllimit='+limit,
                f='&format='+format,
                c='',
                o='')
            else: urlName = urlTemplate.substitute(
                t='&list=backlinks',
                a='&bltitle='+article,
                l='&bllimit='+limit,
                f='&format='+format,
                c='&blcontinue='+cont,
                o='')
        if type=='images':
            ns = 6
            if cont==None: urlName = urlTemplate.substitute(
                t='&prop=images',
                a='&titles='+article,
                l='&imlimit='+limit,
                f='&format='+format,
                c='',
                o='')
            else: urlName = urlTemplate.substitute(
                t='&prop=images',
                a='&titles='+article,
                l='&imlimit='+limit,
                f='&format='+format,
                c='&imcontinue='+cont,
                o='')
        if type=='pages': #gets all pages in a category page, not subcategories
            ns = 0
            if cont==None: urlName = urlTemplate.substitute(
                t='&list=categorymembers',
                a='&cmtitle='+article,
                l='&cmlimit='+limit,
                f='&format='+format,
                c='',
                o='&cmtype=page')
            else: urlName = urlTemplate.substitute(
                t='&list=categorymembers',
                a='&cmtitle='+article,
                l='&cmlimit='+limit,
                f='&format='+format,
                c='&cmcontinue='+cont,
                o='&cmtype=page')
        if type=='categories':
            ns=14
            if cont==None: urlName = urlTemplate.substitute(
                t='&prop=categories',
                a='&titles='+article,
                l='&cllimit='+limit,
                f='&format='+format,
                c='',
                o='')
            else: urlName = urlTemplate.substitute(
                t='&prop=categories',
                a='&titles='+article,
                l='&cllimit='+limit,
                f='&format='+format,
                c='clcontinue='+cont,
                o='')
        jsonData = urllib.urlopen(urlName).read()
        [data, c] = WikiData.parseWikiJson(jsonData, ns, type)
        data.sort() #testing
        if c==None:
            return data
        if c!=None:
            return data 
    
    '''
    Parses the given JSON data to extract the desired links
    *Private
    @param text the text that is the JSON data
    @param ns the ns number corresponding to the desired type of data (0 for article names, 6 for image names)
    @return a list containing the list of elements (index 0) and continue URL (index 1, None if not needed)
    '''
    @staticmethod
    def parseWikiJson(jsonData, ns, type):
        jsonDict = json.loads(jsonData)
        if type=='pages':
            cont = jsonDict.get('query-continue',None)
            if cont!=None:
                cont = jsonDict.get('query-continue',None).get('categorymembers',None).get('cmcontinue',None)
            data = [
                elem.get('title') 
                for elem in jsonDict.get('query', None).get('categorymembers', None) 
                if elem.get('ns', None)==ns
                ]
        elif type=='forward':
            cont = jsonDict.get('query-continue',None)
            if not cont==None:
                cont = jsonDict.get('query-continue',None).get('links',None).get('plcontinue',None)
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
            data = [
                elem.get('title')
                for elem in jsonDict.get('query', None).get('pages', None).get(artNum, None).get('links')
                if (elem.get('ns', None)==ns and elem.get('title',None)[0]!='+' and elem.get('title',None)[0]!='.')
                ]
        elif type=='backward':
            cont = jsonDict.get('query-continue',None)
            if cont!=None:
                cont=jsonDict.get('query-continue',None).get('backlinks',None).get('blcontinue',None)
            data = [
                elem.get('title') 
                for elem in jsonDict.get('query', None).get('backlinks') 
                if elem.get('ns', None)==ns
                ]
        elif type=='images':
            cont = jsonDict.get('query-continue',None)
            if cont!=None:
                cont = jsonDict.get('query-continue',None).get('images',None).get('imcontinue',None)
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
            data = [
                elem.get('title') 
                for elem in jsonDict.get('query', None).get('pages').get(artNum, None).get('images', None) 
                if elem.get('ns', None)==ns
                ]
        elif type=='categories':
            cont = jsonDict.get('query-continue',None)
            if cont!=None:
                cont = jsonDict.get('query-continue',None).get('categories',None).get('clcontinue',None)
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
            data = [
                elem.get('title') 
                for elem in jsonDict.get('query', None).get('pages', None).get(artNum, None).get('categories', None) 
                if elem.get('ns', None)==ns
                ]
        if cont!=None:
            print 'C:',cont.encode('utf-8')
        return [data,cont]
    
    def initializeGame(self):
        country = self.chooseCountry()
        clues = self.chooseClues(country)
        clippings = self.getClippings(country)
        return [country, clues, clippings]
    
    '''
    Chooses a random country from the list of possibilities
    *Private
    '''
    def chooseCountry(self):
        pass
    
    '''
    Gets the clues based on a specific country
    *Private
    '''
    def chooseClues(self, article):
        pass
    
    '''
    Checks whether an article is a person. Some error is possible, because Wikipedia doesn't have a People tag
    @return a boolean representing if article is a person
    *Private (unless needed for some other reason than clues)
    NEED - Testing
    '''
    def isPerson(self, article):
        cats = self.queryDB(article).get('categories', None)
        if a != None:
            for e in cats:
                if (len(e)>=15 and e[9:15]=='People') or e[-6:]=='people':
                    return True
        else:
            return False
    
    '''
    Determines how far away two articles are in Wikipedia. Some error is possible, depending on continuation, and backlinks
    @param art1 the query article (i.e. the country they guessed)
    @param art2 the destination article (i.e. the Country they are trying to guess)
    @returns a integer representing how how away they are (0: same article, 1: one away, 2: more than two away)
    *Public
    NEED - testing (maybe need unicode encodings in query for accuracy, works for ascii)
    '''
    def distanceFrom(self, art1, art2):
        if art1==art2:
            return 0
        else:
            f1 = self.queryDB(art1).get('forward',None)
            if f1!=None and (art2 in f1):
                return 1
            b2 = self.queryDB(art1).get('backward',None)
            if b2!=None and (art1 in b2):
                return 1
            return 2
        
    
    '''
    Gets text clippings from forward links to an article
    *Public
    @returns a list [ getClip1, getClip2, getClip3 ], where each getClipI is list from getClip
    '''
    def chooseClippings(self, article):
        pass
    
    '''
    Gets text clippings from forward links to an article
    *Public
    @returns a list [text, image_name]
    '''
    def getClip(self, article):
        pass
    
    '''
    Provides a unique representation of the shelf
    *Public, but ~3000 pages worth of printing, don't use.
    '''
    def __repr__(self):
        for e in self.wikiCache.get('WhereInWiki',None):
            print e.encode('utf-8')
            dicts = self.wikiCache.get(e.encode('utf-8'))
            for c in dicts.keys():
                print '\t',c
                for t in dicts.get(c,None):
                    print '\t\t',t.encode('utf-8')
        return ''
    
    '''
    Provides a unique representation of the shelf
    *Public, but ~3000 pages worth of printing, don't use.
    '''
    def __str__(self):
        return self.__repr__()
    
if __name__=='__main__':
    PLAY = False
    if PLAY:
        pass
    else:
        w = WikiData()
        for c in w.wikiCache.get('WhereInWiki'):
            print c.encode('utf-8')
            w.queryDB(c)
        w.close()
        

#NOTES
#    If forward link start with + or . just ignore