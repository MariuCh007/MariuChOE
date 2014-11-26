import os
import time
import glob
import urllib2

import xbmc
import utils

CacheDir  = xbmc.translatePath(os.path.join(utils.ADDON.getAddonInfo('profile'), 'cache'))
CacheSize = 100


def checkCacheDir():
    if not os.path.isdir(CacheDir):
        os.makedirs(CacheDir)


def getURLNoCache(url, agent=None):
    req = urllib2.Request(url)
    if agent:
        req.add_header('User-Agent', agent)

    response = urllib2.urlopen(req)
    html     = response.read()
    response.close()
    return html.replace('\r', '').replace('\n', '').replace('\t', '')


def getURL(url, maxSec=0, agent=None):
    purgeCache()
    
    if url == None:
        return None

    if maxSec > 0:
        timestamp = getTimestamp(url)
    if timestamp > 0:
        if (time.time() - timestamp) <= maxSec:
            return getCachedData(url)
			
    data = getURLNoCache(url, agent)
    addToCache(url, data)
    return data


def getTimestamp(url):
    cacheKey  = createKey(url)
    cachePath = os.path.join(CacheDir, cacheKey)

    if os.path.isfile(cachePath):
        try:    return os.path.getmtime(cachePath)
        except: pass

    return 0


def getCachedData(url):
    cacheKey  = createKey(url)
    cachePath = os.path.join(CacheDir, cacheKey)
    f         = file(cachePath, 'r')

    data = f.read()
    f.close()

    return data


def addToCache(url, data):
    checkCacheDir()

    cacheKey  = createKey(url)
    cachePath = os.path.join(CacheDir, cacheKey)
    f         = file(cachePath, 'w')

    f.write(data)
    f.close()

    purgeCache()


def createKey(url):
    try:
        from hashlib import md5
        return md5(url).hexdigest()
    except:
        import md5
        return md5.new(url).hexdigest()

        
def purgeCache():
    files  = glob.glob(os.path.join(CacheDir, '*'))
    nFiles = len(files)

    try:
        while nFiles > gCacheSize:            
            oldestFile = getOldestFile(files)
            path       = os.path.join(CacheDir, oldestFile)
 
            while os.path.exists(path):
                try:    os.remove(path)
                except: pass

            files  = glob.glob(os.path.join(CacheDir, '*'))
            nFiles = len(files)
    except:
        pass


def getOldestFile(files):
    if not files:
        return None
    
    now    = time.time()
    oldest = files[0], now - os.path.getctime(files[0])

    for f in files[1:]:
        age = now - os.path.getctime(f)
        if age > oldest[1]:
            oldest = f, age

    return oldest[0]