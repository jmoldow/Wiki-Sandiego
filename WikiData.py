import json
import shelve
import string
import urllib
import random
import warnings
import re

DEBUG=True

class WikiData:
    '''
    Provides methods for easily manipuating data from Wikipedia.
    Uses the API at http://en.wikipedia.org/w/api.php.
    NEED - refactor code so that not all methods show up as public, try/catch statements for queryBD, text playing(?)
    '''
    def __init__(self, name='wikiCache'):
        '''
        Initializes the WikiData class
        '''
        self.initializeDB(name)

    def initializeDB(self, name):
        '''
        Initializes the database. Creates the database file if needed, and loads it into the instance of the class.
        *Private
        @param name The name of the desired database to check/create
        @return boolean Returns true if the database needed to be created.
        '''
        self.wikiCache = shelve.open(name)
        if self.wikiCache.get('WhereInWiki',None)==None:
            self.wikiCache['WhereInWiki'] = self.getAllCountries()
            self.wikiCache.sync()

    def queryDB(self, query):
        '''
        Queries the database for a specific entry, adding it if need be.
        *Public
        @param query A article to query in the database
        '''
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

    def close(self):
        '''
        Closes the class, properly storing the cache.
        *Public
        '''
        self.wikiCache.close()
        
    def getAllCountries(self):
        '''
        Gets the set of most countries (169/~196).
        @return a sorted list of country names (in utf-8)
        *Private
        '''
        countries = set([])
        countries.update( self.getArticleLinks('Category:Northern_American_countries','pages') )
        countries.update( self.getArticleLinks('Category:Central_American_countries','pages') )
        countries.update( self.getArticleLinks('Category:South_American_countries','pages') )
        countries.update( self.getArticleLinks('Category:European_countries','pages') )
        countries.update( self.getArticleLinks('Category:Southeast_Asian_countries','pages') )
        countries.update( self.getArticleLinks('Category:East_Asian_countries','pages') )
        countries.update( self.getArticleLinks('Category:African_countries','pages') )
        countries.update( self.getArticleLinks('Category:Middle_Eastern_countries','pages') )
        countries.update( self.getArticleLinks('Category:Western_Asian_countries','pages') )
        countries.update( self.getArticleLinks('Category:South_Asian_countries','pages') )
        countries.update( self.getArticleLinks('Category:Near_Eastern_countries','pages') )
        #Get rid of the following articles, not actually countries:
        countries.discard('List of sovereign states and dependent territories in Africa')
        countries.discard('Flags of Africa')
        countries.discard('List of African countries by Human Development Index')
        countries.discard('List of African countries by population density')
        countries.discard('List of sovereign states and dependent territories in South America')
        countries.discard('List of sovereign states and dependent territories in Europe')
        countries.discard('European microstates')
        countries.discard('List of Middle East countries by population')
        countries.discard(None)
        countries = list(countries)
        countries.sort()
        return countries
    
    def getArticleLinks(self, article, type, cont=None, limit='500', format='json'):
        '''
        Returns a the requested query type on the given article.
        *Private
        @param type the type of links that you want ('forward', 'backward', 'images', 'pages', 'categories', 'encode')
        @param article The name of the article (with or without whitespace)
        @param cont the entire string nested in query continue(None by default)
        @return a list of all of the desired links
        NEED error handling, continuation(unicode is making this annoying, is 500 okay?)
        '''
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            if article.encode('utf-8')==article: #Gets rid of countries with odd characters
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
                if type=='export':
                    ns=0
                    urlName = urlTemplate.substitute(
                        t='&export',
                        a='&titles='+article,
                        l='',
                        f='&format='+format,
                        c='',
                        o='')
                jsonData = urllib.urlopen(urlName).read()
                [data, c] = self.parseWikiJson(jsonData, ns, type, article)
#                data.sort() 
#                if c==None:
#                    return data
#                if c!=None:
#                    return data 

                return data
    def parseWikiJson(self, jsonData, ns, type, article):
        '''
        Parses the given JSON data to extract the desired links
        *Private
        @param text the text that is the JSON data
        @param ns the ns number corresponding to the desired type of data (0 for article names, 6 for image names) [Ignored if type==encode]
        @return a list containing the list of elements (index 0) and continue URL (index 1, None if not needed)
        WANT - export to get rid of formatting
        '''
        jsonDict = json.loads(jsonData)
        if type=='pages':
            cont = jsonDict.get('query-continue',None)
            if cont!=None:
                cont = jsonDict.get('query-continue',None).get('categorymembers',None).get('cmcontinue',None)
            data = [
                elem.get('title') 
                for elem in jsonDict.get('query', None).get('categorymembers', None) 
                if (elem.get('ns', None)==ns and elem.get('title').encode('utf-8')==elem.get('title') )
                ]
        elif type=='forward':
            cont = jsonDict.get('query-continue',None)
            if not cont==None:
                cont = jsonDict.get('query-continue',None).get('links',None).get('plcontinue',None)
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
            data = [
                elem.get('title')
                for elem in jsonDict.get('query', None).get('pages', None).get(artNum, None).get('links')
                if (elem.get('ns', None)==ns and elem.get('title').encode('utf-8')==elem.get('title')  and elem.get('title',None)[0]!='+' and elem.get('title',None)[0]!='.')
                ]
        elif type=='backward':
            cont = jsonDict.get('query-continue',None)
            if cont!=None:
                cont=jsonDict.get('query-continue',None).get('backlinks',None).get('blcontinue',None)
            data = [
                elem.get('title') 
                for elem in jsonDict.get('query', None).get('backlinks') 
                if (elem.get('ns', None)==ns and elem.get('title').encode('utf-8')==elem.get('title'))
                ]
        elif type=='images':
            cont = jsonDict.get('query-continue',None)
            if cont!=None:
                cont = jsonDict.get('query-continue',None).get('images',None).get('imcontinue',None)
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
            if jsonDict.get('query', None).get('pages').get(artNum, None).get('images', None)!=None:
                data = [
                    elem.get('title') 
                    for elem in jsonDict.get('query', None).get('pages').get(artNum, None).get('images', None) 
                    if (elem.get('ns', None)==ns and elem.get('title').encode('utf-8')==elem.get('title') )
                    ]
            else:
                data=[]
        elif type=='categories':
            cont = jsonDict.get('query-continue',None)
            if cont!=None:
                cont = jsonDict.get('query-continue',None).get('categories',None).get('clcontinue',None)
            artNum = jsonDict.get('query', None).get('pages', None).keys()[0]
            data = [
                elem.get('title') 
                for elem in jsonDict.get('query', None).get('pages', None).get(artNum, None).get('categories', None) 
                if (elem.get('ns', None)==ns and elem.get('title').encode('utf-8')==elem.get('title') )
                ]
        elif type=='export':
            cont = jsonDict.get('query-continue',None)
            data = jsonDict.get('query', None).get('export', None).get('*', None)
            end = data.find("==") #finds end of introduction
            start = data.rfind("'''",0,end)
            start = data.rfind("'''",0,start) #accounts for countries whose name is not the exact title
            data = data[start: end]
            proRegEx = re.compile('\(\{\{[^)?]*\)')
            for m in proRegEx.finditer(data):
                if data[m.start():m.start()+3]=='({{': #not sure why my regex is catching errors
                    data = data[0:m.start()]+data[m.end():-1] #delete entirely
            data.replace(article,'[REDACTED]')
        if cont!=None: #ignore continuations for now
            pass
        return [data,cont]
    
    @staticmethod
    def checkCountry(country, title):
        '''
        Returns true if it is a valid title.
        '''
        a = str([c for c in country.lower() if 'a'<=c<='z'])
        b = str([c for c in title.lower() if 'a'<=c<='z'])
        return b.find(a) == -1
    
    def initializeGame(self):
        '''
        Returns all the needed information to start the game
        @return a list of the form [ Carmen's location , [clues] , [ list of clippings ] ]
        '''
        country = self.chooseCountry()
        clues = self.chooseClues(country)
        clippings = self.chooseClippings(country)
        return [country, clues, clippings]

    def chooseCountry(self):
        '''
        Chooses a random country from the list of possibilities
        *Private
        @return a unicode string of the country name
        NEED - Testing
        '''
        countries = self.queryDB('WhereInWiki')
        return random.choice(countries)

    def chooseClues(self, article):
        '''
        Gets the clues based on a specific country
        *Private
        NEED - Testing
        '''
        countries = self.queryDB(article)
        back = countries.get('backward')
        if back<=9:
            return back #probably raise error later, that way we can guarentee 9, shouldn't actually happen
        else:
            clues = []
            while len(clues)<9:
                c = random.choice(back)
                if c not in clues and self.checkCountry(article, c):
#                    print '\t',c.encode('utf-8')
                    clues.append(c)
            return clues

    def isPerson(self, article):
        '''
        Checks whether an article is a person. Some error is possible, because Wikipedia doesn't have a People tag
        @return a boolean representing if article is a person
        *Private (unless needed for some other reason than clues)
        NEED - Testing, better metrics?
        '''
        cats = self.queryDB(article).get('categories', None)
        if a != None:
            for e in cats:
                if (len(e)>=15 and e[9:15]=='People') or e[-6:]=='people':
                    return True
        else:
            return False

    def distanceFrom(self, art1, art2):
        '''
        Determines how far away two articles are in Wikipedia. Some error is possible, depending on continuation, and backlinks
        @param art1 the query article (i.e. the country they guessed)
        @param art2 the destination article (i.e. the Country they are trying to guess)
        @returns a integer representing how how away they are (0: same article, 1: one away, 2: more than two away)
        *Public
        NEED - testing (maybe need unicode encodings in query for accuracy, works for ascii), do we even need this currently?
        '''
        if art1==art2:
            return 0
        else:
            f1 = self.queryDB(art1).get('forward',None)
            if f1!=None and (art2 in f1):
                return 1
            b2 = self.queryDB(art1).get('backward',None)
            if b2!=None and (art1 in b2):
                return 1
            if f1!=None and b2!=None:
                s = set(b2)
                for e in f1:
                    if e in s:
                        return 2
            return 3


    def chooseClippings(self, article):
        '''
        Gets clippings from forward links to an article
        *Public
        @returns a dictionary {article1:getClip1, article2:getClip2, article3:getClip3}, where each getClipI is list from getClip
        NEED - Testing, ignore articles with name of country in it?
        '''
        countries = self.queryDB(article)
        forward = countries.get('forward')
        clues = dict([])
        if forward<=3:
            for f in forward: clues[f.encode('utf-8')] = self.getClip(c)
            return forward #probably raise error later, that way we can guarentee 9, doubtful will ever happen
        else:
            while len(clues)<3:
                c = random.choice(forward)
                if c not in clues:
                    clues[c.encode('utf-8')] = self.getClip(c)
            return clues
        pass

    def getClip(self, article):
        '''
        Gets clippings from a specific article
        *Private
        @returns a list [text, image_name]
        NEED to implement
        '''
        text = self.getArticleLinks(article, 'export')
        art = self.queryDB(article)
        images = art.get('images',None)
        if images==[]: return [text, None]
        else: return [text, images[0]]

    def __repr__(self):
        '''
        Provides a unique representation of the shelf
        *Public, but ~3000 pages worth of printing, don't use.
        '''
        for e in self.wikiCache.get('WhereInWiki',None):
            print e.encode('utf-8')
            dicts = self.wikiCache.get(e.encode('utf-8'))
            for c in dicts.keys():
                print '\t',c
                for t in dicts.get(c,None):
                    print '\t\t',t.encode('utf-8')
        return ''

    def __str__(self):
        '''
        Provides a unique representation of the shelf
        *Public, but ~3000 pages worth of printing, don't use.
        '''
        return self.__repr__()

if __name__=='__main__':
    pass
    PLAY = False
    if PLAY:
        pass
    else:
        w = WikiData('test')
        w.initializeGame()
        
#        for c in w.wikiCache.get('WhereInWiki'):
#            with warnings.catch_warnings():
#                warnings.simplefilter('ignore')
#                if c.encode('utf-8')==c:
#                    print '\n',c
#                    w.chooseClues(c)
                
                
#        for c in w.wikiCache.get('WhereInWiki'):
#            if c.encode('utf-8')!=c:
#                pass
#            else: print c
#            w.queryDB(c)
#        w.close()
