import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os
import shutil
import urllib2,urllib
import re
import extract
import downloader
import time

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='http://www.thelittleblackbox.nl/wizard_packs/'
ADDON=xbmcaddon.Addon(id='plugin.video.tlbbocs')
VERSION = "1.0.1"
PATH = "TLBB Wizard"            
    
def CATEGORIES():
    username = ADDON.getSetting('username')
    password = ADDON.getSetting('password')
    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version < 14:
        xbmcversion = '0'
    else:
        xbmcversion = '1'

    if ADDON.getSetting('adult') == 'true':
        adult = 1
    else:
        adult = 0
    
    if ADDON.getSetting('login') == 'true':
        buildsURL = 'http://cloud.thelittleblackbox.co.uk/community_builds.txt?u=%s&p=%s&kodi=%s&adult=%s' % (username, password, xbmcversion, adult)
    else:
        buildsURL = 'http://cloud.thelittleblackbox.co.uk/community_builds.txt?u=none&p=none&kodi=%s&adult=%s' % (xbmcversion, adult)
    link = OPEN_URL(buildsURL).replace('\n','').replace('\r','')
    print "Generated URL : " + str(buildsURL)
    print "Kodi : " + str(xbmcversion)
    print "Adult : " + str(adult)
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,1,iconimage,fanart,description)
    setView('movies', 'MAIN')
    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description):
        choice = xbmcgui.Dialog().yesno('The ' +name +' build', description, 'Would you like to install?', nolabel='Cancel',yeslabel='Accept')
        if choice == 0:
            return
        elif choice == 1:
            choice = xbmcgui.Dialog().yesno('WARNING', 'YOU WILL LOSE ALL EXISTING SETTINGS', '', 'Are you sure you want to continue?', nolabel='Cancel',yeslabel='Accept')
        if choice == 0:
            return
        elif choice == 1:
            import downloader
            incremental = 'http://cloud.thelittleblackbox.co.uk/cloud/incrementcount.php?linkx=%s' % (url)
            OPEN_URL(incremental)
            dest = '/storage/.restore/'
            path = os.path.join(dest, '20141128094249.tar')

            if not os.path.exists(dest):
                try: os.makedirs(dest)
                except: pass

            downloader.download(url, path)



def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
                
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
                
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        wizard(name,url,description)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

