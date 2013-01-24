# -*- coding: utf-8 -*-

# Импортируем нужные нам библиотеки
import urllib, urllib2, re, sys, os
import xbmcplugin, xbmcgui
from BeautifulSoup import BeautifulSoup

pluginhandle = int(sys.argv[1])
#settings = xbmcaddon.Addon(id='plugin.video.m24_ru')
#translation = settings.getLocalizedString

videoPattern = "http://b1.m24.ru/c/%s.1.mp4"

def index():
    soup = getHtml("/videos/")        
    t = soup.find('div', attrs={'class' : 'SwitchMenuType3'}).findAll('a')
    for i in t:
        title = str(i.span.contents[0]).decode('utf8')
        url = str(i['href']).decode('utf8')
        addDir(title, url, 2)
    addDir("Программы по категориям", '/videos?type=programs', 3)
    addLink("M24 Live Stream", liveStream(), '')
    
def programCat(url):
    soup = getHtml(url)        
    t = soup.find('div', attrs={'class' : 'SwitchMenuType2'}).findAll('a')
    for i in t:
        title = str(i.span.contents[0]).decode('utf8')
        url = str(i['href']).decode('utf8')
        addDir(title, url, 2)
	
def listVideos(url, page = 1):
    addDir("Список разделов", "", 0)
    soup = getHtml(url)
    video = soup.find('div', attrs={'id' : 'VideosList'}).findAll('a')
    for vi in video:
        title = str(vi.contents[2]).decode('utf8').strip().replace("&quot;", '"')
        imgUrl = str(vi.img['src']).decode('utf8')
        videoUrl = re.compile(".+?/([0-9]+)\..+?").findall(imgUrl)[0]
        videoUrl = videoPattern % videoUrl
#        print title, url, videoUrl
        addLink(title, videoUrl, imgUrl)
    if page == 1:
        newUrl = url + '&page=2'
    else:
        newUrl = re.sub(r'page=[0-9]+', 'page='+str(page+1), url)
    addDir("Следующая страница ("+str(page+1)+")", newUrl, 2, page+1)
    
#        t = re.findall("page=[0-9]+", url)
#    newUrl = re.sub(r'page=[0-9]+', 'page='+str(page+1), url)
#        addDir(str(t), newUrl, 2)
    return 1
	
def liveStream():
        content = getUrl("http://tv.m24.ru/")
        url = re.compile('src=\"(http:\/\/player.rutv.ru.+?)\"', re.DOTALL).findall(content)[0]
        player = getUrl(url)
        url = re.compile('\"video\":\"(.+?)\"', re.DOTALL).findall(player)[0]
        url = url.replace('\\', '')
        return url+' live=true timeout=60'
        #listitem = xbmcgui.ListItem(path=url)
        #return xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)	

def parameters_string_to_dict(parameters):
        ''' Convert parameters encoded in a URL to a dict. '''
        paramDict = {}
        if parameters:
            paramPairs = parameters[1:].split("&")
            for paramsPair in paramPairs:
                paramSplits = paramsPair.split('=')
                if (len(paramSplits)) == 2:
                    paramDict[paramSplits[0]] = paramSplits[1]
        return paramDict

def addLink(title, url, thumb, mode = 0):
#    url = url + '?mode='+str(mode)
    item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=thumb)
    item.setInfo( type='Video', infoLabels={'Title': title} )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)


def addDir(title, url, mode, page = 1):
#sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode)) + '&page=' + str(page)
    item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    item.setInfo( type='Video', infoLabels={'Title': title} )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)

def getHtml(url):
    base = 'http://www.m24.ru'
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3', 'Content-Type':'application/x-www-form-urlencoded'}
    conn = urllib2.urlopen(urllib2.Request(base+url, None, headers))
    """urllib.urlencode({'type': 'sprojects'})"""
    html = conn.read()
    conn.close()
    soup = BeautifulSoup(html, fromEncoding="utf-8")
    return soup

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        response = urllib2.urlopen(req,timeout=30)
        link = response.read()
        response.close()
        return link

params=parameters_string_to_dict(sys.argv[2])
url=None
mode=None

try:
        url = urllib.unquote_plus(params["url"])
except:
        pass
try:
        mode = int(params["mode"])
except:
        pass
try:
        page = int(params["page"])
except:
        page = 1
        pass    
xbmc.log(str(url))

if mode==None or url==None or len(url)<1:
        index()
       
elif mode==2:
        listVideos(url, page)
elif mode==9:
        liveStream()
elif mode==3:
        programCat(url)
"""elif mode==2:
        playVideo(url)
elif mode==7:
        listVideos(url)
elif mode==9:
        liveStream() """

xbmcplugin.endOfDirectory(pluginhandle)

    

#index()
#listVideos('/videos?type=popular')
