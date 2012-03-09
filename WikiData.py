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
    def __init__(self, name='wikicache'):
        self.limit='500'
        self.format='json'
        self.name=name
        self.initializeDB(self.name)
        
    '''
    Initializes the database. Creates the database file if needed, and loads it into the instance of the class.
    @param name The name of the desired database to check/create
    @return boolean Returns true if the database needed to be created.
    NEED - error handling
    '''
    def initializeDB(self, name):
#        wikiCache['WhereInWiki'] = SetOfAllCountries (or whatever we are using as the possible starting points)
#        wikiCache[articleName] = { 'forward':forwardLinksStringSet, 'backward':backwardLinkStringSet }
		self.wikiCache = shelve.open(name)
		if self.wikiCache.get('WhereInWiki',None)==None:
			self.wikiCache['WhereInWiki'] = self.getAllCountries()
			self.wikiCache.sync()

    '''
    Queries the database for a specific entry, adding it if need be.
    @param query A article to query in the database
    
    NEED - error handling, testing, more data in wikiShelf?
    '''
    def queryDB(self, query):
        query = query.encode('utf-8')
        if query=='WhereInWiki' and self.wikiCache.get('WhereInWiki',None)==None:
            self.wikiCache['WhereInWiki'] = self.getAllCountries()
        elif str(query) not in self.wikiCache:
            self.wikiCache[str(query)] = { 'forward':self.getArticleLinks(query,'forward'), 'backward':self.getArticleLinks(query,'backward'), 'images':self.getArticleLinks(query,'images'), 'categories': self.getArticleLinks(query,'categories')} #NEED
        return self.wikiCache.get(str(query),None)
    
    '''
    Closes the class, properly storing the cache.
    '''
    def close(self):
        self.wikiCache.close()
    
    '''
    Gets the set of all countries and adds them to the database for future use.
    NEED - error handling, testing
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
            if cont==None: urlName = urlTemplate.substitute(t='&prop=links',a='&titles='+article, l='&pllimit='+limit, f='&format='+format, c='', o='')
            else: urlName = urlTemplate.substitute(t='&prop=links',a='&titles='+article, l='&pllimit='+limit, f='&format='+format, c='&plcontinue='+cont, o='')
        if type=='backward':
            ns = 0
            if cont==None: urlName = urlTemplate.substitute(t='&list=backlinks',a='&bltitle='+article, l='&bllimit='+limit, f='&format='+format, c='', o='')
            else: urlName = urlTemplate.substitute(t='&list=backlinks',a='&bltitle='+article, l='&bllimit='+limit, f='&format='+format, c='&blcontinue='+cont, o='')
        if type=='images':
            ns = 6
            if cont==None: urlName = urlTemplate.substitute(t='&prop=images',a='&titles='+article, l='&imlimit='+limit, f='&format='+format, c='', o='')
            else: urlName = urlTemplate.substitute(t='&prop=images',a='&titles='+article, l='&imlimit='+limit, f='&format='+format, c='&imcontinue='+cont, o='')
        if type=='pages': #gets all pages in a category page, not subcategories
            ns = 0
            if cont==None: urlName = urlTemplate.substitute(t='&list=categorymembers',a='&cmtitle='+article, l='&cmlimit='+limit, f='&format='+format, c='', o='&cmtype=page')
            else: urlName = urlTemplate.substitute(t='&list=categorymembers',a='&cmtitle='+article, l='&cmlimit='+limit, f='&format='+format, c='&cmcontinue='+cont, o='&cmtype=page')
        if type=='categories':
            ns=14
            if cont==None: urlName = urlTemplate.substitute(t='&prop=categories',a='&titles='+article, l='&cllimit='+limit, f='&format='+format, c='', o='')
            else: urlName = urlTemplate.substitute(t='&prop=categories',a='&titles='+article, l='&cllimit='+limit, f='&format='+format, c='clcontinue='+cont, o='')
        jsonData = urllib.urlopen(urlName).read()
        [data, c] = WikiData.parseWikiJson(jsonData, ns, type)
        if c==None:
            return data
        if c!=None:
            return data 
    
    '''
    Parses the given JSON data to extract the desired links
    @param text the text that is the JSON data
    @param ns the ns number corresponding to the desired type of data (0 for article names, 6 for image names)
    @return a list containing the list of elements (index 0) and continue URL (index 1, None if not needed)
    NEED - continuation
    '''
    @staticmethod
    def parseWikiJson(jsonData, ns, type):
        jsonDict = json.loads(jsonData)
#        print jsonDict
        if type=='pages':
            data = [ elem.get('title') for elem in jsonDict.get('query', None).get('categorymembers', None) if elem.get('ns', None)==ns]
        elif type=='forward':
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
            data = [ elem.get('title') for elem in jsonDict.get('query', None).get('pages', None).get(artNum, None).get('links') if (elem.get('ns', None)==ns and elem.get('title',None)[0]!='+' and elem.get('title',None)[0]!='.')]
        elif type=='backward':
            data = [ elem.get('title') for elem in jsonDict.get('query', None).get('backlinks') if elem.get('ns', None)==ns]
        elif type=='images':
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
#            print 'Images JSON:',jsonDict.get('query', None).get('pages').get(artNum, None).get('images', None)
            data = [ elem.get('title') for elem in jsonDict.get('query', None).get('pages').get(artNum, None).get('images', None) if elem.get('ns', None)==ns]
        elif type=='categories':
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
#            print 'Categories JSON:',jsonDict.get('query', None).get('pages', None).get(artNum, None).get('categories', None)
            data = [ elem.get('title') for elem in jsonDict.get('query', None).get('pages', None).get(artNum, None).get('categories', None) if elem.get('ns', None)==ns]
        if jsonDict.get('query_continue', None)==None:
            return [data,None]
        else:
            return [data, None] #add ability to get more
#        'query-continue'
#            'links'
#                'plcontinue'
#                    string (e.g. "3354|0|Karlshorst")

    def chooseClues(self, article):
        pass
    
    def __repr__(self):
        for e in self.wikiCache.get('WhereInWiki',None):
            print e.encode('utf-8')
            dicts = self.wikiCache.get(e.encode('utf-8'))
            for c in dicts.keys():
                print '\t',c
                for t in dicts.get(c,None):
                    print '\t\t',t.encode('utf-8')
        return ''
    
    def __str__(self):
        return self.__repr__()
    
if __name__=='__main__':
    w = WikiData()
    for c in w.wikiCache.get('WhereInWiki'):
        print c.encode('utf-8')
        w.queryDB(c)
    print w
    w.close()

#NOTES
#    If forward link start with + or . just ignore