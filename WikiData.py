'''
Provides methods for easily manipuating data from Wikipedia.
Uses the API at http://en.wikipedia.org/w/api.php.
'''
class WikiData:
    limit=500
    format='json'
    
    '''
    Returns a set of all articles that are linked from a given article.
    @param article The name of the article (with or without whitespace)
    '''
    def getArticleLinks(article):
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
    
#http://en.wikipedia.org/wiki/Category:Northern_American_countries
#http://en.wikipedia.org/wiki/Category:Central_American_countries
#http://en.wikipedia.org/wiki/Category:South_American_countries
#http://en.wikipedia.org/wiki/Category:European_countries
#http://en.wikipedia.org/wiki/Category:Southeast_Asian_countries
#http://en.wikipedia.org/wiki/Category:East_Asian_countries
#http://en.wi