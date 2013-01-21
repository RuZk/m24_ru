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
#		print title, url
        addDir(title, url, 2)

def listVideos(url):
    soup = getHtml(url)
    video = soup.find('div', attrs={'id' : 'VideosList'}).findAll('a')
    for vi in video:
        title = str(vi.contents[2]).decode('utf8').strip().replace("&quot;", '"')
        url = str(vi.img['src']).decode('utf8')
        videoUrl = re.compile(".+?/([0-9]+)\..+?").findall(url)[0]
        videoUrl = videoPattern % videoUrl
#        print title, url, videoUrl
        addLink(title, videoUrl, url)
    #next page
    return 1

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

def addLink(title, url, thumb):
    item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=thumb)
    item.setInfo( type='Video', infoLabels={'Title': title} )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)


def addDir(title, url, mode):
#sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))
    sys_url = sys.argv[0] + '?url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))
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

params=parameters_string_to_dict(sys.argv[2])
url=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass


if mode==None or url==None or len(url)<1:
        index()
       
elif mode==2:
        listVideos(url)
"""elif mode==2:
        playVideo(url)
elif mode==7:
        listVideos(url)
elif mode==9:
        liveStream() """

xbmcplugin.endOfDirectory(pluginhandle)

    

#index()
#listVideos('/videos?type=popular')
