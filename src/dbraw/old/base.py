""" Music DB Raw Data Bases Class """

__all__ = ["RawData", "RawArtistMediaData", "RawArtistProfileData", "RawDataBase", "RawNameData", "RawMetaData", "RawIDData", "RawURLData",
           "RawURLInfoData", "RawPageData", "RawProfileData", "RawMediaData", "RawMediaReleaseData", "RawMediaAlbumData", 
           "RawMediaCountsData", "RawFileInfoData", "RawTextData", "RawLinkData", "RawTagData", "RawMediaMetaData"]


from utils import FileIO, HTMLIO, FileInfo
from datetime import datetime
from math import ceil, floor
from copy import copy, deepcopy
from bs4 import BeautifulSoup,element
from pandas import Series, DataFrame
from .mdbartistname import MusicDBArtistName


def printAll():
    for rdbclass in __all__:
        print("    ###################################################################################")
        print("    def make{0}(self, *args, **kwargs): return {0}(*args, **kwargs)".format(rdbclass))
        print("    def is{0}(self, arg): return isinstance(arg, {0})".format(rdbclass))
        print("")


#####################################################################################################################
# Main Raw Base Classes
#####################################################################################################################
class RawBaseData:
    def __init__(self):
        self.err = None
        
    def get(self):
        return self.__dict__
        
###################################################
# Primary Artist ID Class
###################################################
class RawIDData(RawBaseData):
    def __init__(self, ID, err=None):
        assert isinstance(ID,str), f"ID [{ID}] is not a string in RawIDData"
        self.ID=ID
        
###################################################
# Primary Artist URL Class
###################################################
class RawURLData(RawBaseData):
    def __init__(self, url, err=None):
        assert isinstance(url,str), f"URL [{url}] is not a string in RawURLData"
        self.url=url
        
###################################################
# Primary Artist Name Class
###################################################
class RawNameData(RawBaseData):
    def __init__(self, name, native=None, err=None):
        assert isinstance(name,str), f"Name [{name}] is not a string in RawNameData"
        self.name  = name
        self.natve = native if isinstance(native,str) is None else name
        
###################################################
# Primary Site MetaData Class
###################################################
class RawMetaData(RawBaseData):
    def __init__(self, title, url, err=None):
        assert isinstance(title,str), f"Title [{title}] is not a string in RawMetaData"
        self.title = title
        assert isinstance(url,str), f"URL [{url}] is not a string in RawMetaData"
        self.url   = url 

###################################################
# Primary Site Pagination Class
###################################################
class RawPageData(RawBaseData):
    def __init__(self, ppp=None, tot=None, more=None, redo=None, err=None):
        assert isinstance(ppp,int) or ppp is None, f"ppp [{ppp}] is not an int or None in RawPageData"
        self.ppp   = ppp
        assert isinstance(tot,int) or tot is None, f"tot [{ppp}] is not an int or None in RawPageData"
        self.tot   = tot
        self.pages = int(ceil(tot/ppp)) if (isinstance(ppp, int) and isinstance(tot, int)) else None
        assert isinstance(more,bool) or more is None, f"More [{more}] is not a bool or None in RawPageData"
        self.more  = more
        assert isinstance(redo,bool) or more is None, f"Redo [{redo}] is not a bool or None in RawPageData"
        self.redo  = redo

###################################################
# Primary Artist Profile Class
###################################################
class RawProfileData(RawBaseData):
    def __init__(self, general=None, genres=None, tags=None, external=None, extra=None, err=None):
        assert isinstance(general,dict) or general is None, f"general [{general}] is not a dict or None in RawProfileData"
        self.general  = general
        assert isinstance(genres,dict) or genres is None, f"genres [{genres}] is not a dict or None in RawProfileData"
        self.genres   = genres
        assert isinstance(tags,dict) or tags is None, f"tags [{tags}] is not a dict or None in RawProfileData"
        self.tags     = tags
        assert isinstance(external,dict) or external is None, f"external [{external}] is not a dict or None in RawProfileData"
        self.external = external
        assert isinstance(extra,dict) or extra is None, f"extra [{extra}] is not a dict or None in RawProfileData"
        self.extra    = extra
    

#####################################################################################################################
# Utility Raw Base Classes
#####################################################################################################################
class RawLinkData:
    def __init__(self, link, err=None):
        self.href  = None
        self.title = None
        self.text  = None
        self.err   = None
        
        if isinstance(link, element.Tag):
            self.href  = link.attrs.get('href')
            self.title = link.attrs.get('title')
            self.text  = link.text
        else:
            self.err = "NoLink"
        
    def get(self):
        return self.__dict__
    

class RawTagData:
    def __init__(self, tag, err=None):
        self.bstag = None
        self.err   = None
        
        if isinstance(tag, element.Tag):
            self.bstag = deepcopy(tag)
        else:
            self.err = "NoTag"
            
    def getTag(self):
        return self.bstag
        
    def get(self):
        return self.__dict__
    

class RawTextData:
    def __init__(self, text, err=None):        
        self.err   = None
        self.text = deepcopy(text.text.strip()) if isinstance(text, element.Tag) else text.strip()
            
    def get(self):
        return self.__dict__
    

class RawMediaData:
    def __init__(self, media={}, err=None):
        self.media = media
        self.err   = err
        
    def get(self):
        return self.__dict__
    

class RawMediaCollection:
    def __init__(self, collection):
        self.collection = collection
        assert isinstance(self.collection,dict), f"Media Collection [{collection}] is not correctly formatted in RawMediaCollection"
        
    def get(self):
        return self.__dict__
    

class RawMediaMetaData:
    def __init__(self, mid, mtype, name):
        self.mid   = str(mid) if isinstance(mid,int) else mid
        assert isinstance(self.mid,str), f"Media ID [{mid}] is not correctly formatted in RawMediaBaseData"
        self.mtype  = mtype
        assert isinstance(self.mtype,str), f"Media Type [{mtype}] is not correctly formatted in RawMediaBaseData"
        self.name  = name
        assert isinstance(self.name,str), f"Media Name [{name}] is not correctly formatted in RawMediaBaseData"
        
    def get(self):
        return self.__dict__
    

class RawMediaReleaseData:
    def __init__(self, album=None, url=None, aclass=None, aformat=None, artist=None, code=None, year=None, err=None):
        self.album   = album
        self.url     = url
        self.aclass  = aclass
        self.aformat = aformat
        self.artist  = artist
        self.code    = code
        self.year    = year
        self.err     = err
        
    def get(self):
        return self.__dict__
    

class RawMediaAlbumData:
    def __init__(self, url=None, album=None, aformat=None, err=None):
        self.url     = url
        self.album   = album
        self.aformat = aformat
        self.err     = err        
        
    def get(self):
        return self.__dict__

    
class RawMediaCountsData:
    def __init__(self, counts={}, err=None):
        self.counts = counts
        self.err    = err
        
    def get(self):
        return self.__dict__
    
    

class RawURLInfoData:
    def __init__(self, name=None, url=None, ID=None, err=None):
        self.name = name
        self.url  = url
        self.ID   = ID
        self.err  = err
        
    def get(self):
        return self.__dict__
    

class RawFileInfoData:
    def __init__(self, info=None, err=None):
        self.called = datetime.now()        
        if info is not None:
            try:
                self.created  = FileInfo(info).time()
            except:
                self.created  = None
            self.filename = info if isinstance(info,str) else None
        else:
            self.created  = None
            self.filename = None
            self.err      = "NoFileInfo"
        
    def get(self):
        return self.__dict__
    

#####################################################################################################################
# Raw Data Class
#####################################################################################################################
class RawData:
    def __init__(self, artist=None, meta=None, url=None, ID=None, pages=None, profile=None, media=None, mediaCounts=None, info=None, err=None):
        self.artist      = artist if isinstance(artist,RawNameData) else RawNameData()
        self.meta        = meta if isinstance(meta,RawMetaData) else RawMetaData()
        self.url         = url if isinstance(url,RawURLData) else RawURLData()
        self.ID          = ID if isinstance(ID,RawIDData) else RawIDData()
        self.pages       = pages if isinstance(pages,RawPageData) else RawPageData()
        self.profile     = profile if isinstance(profile,RawProfileData) else RawProfileData()
        self.media       = media if isinstance(media,RawMediaData) else RawMediaData()
        self.mediaCounts = mediaCounts if isinstance(mediaCounts,RawMediaCountsData) else RawMediaCountsData()
        self.info        = info if isinstance(info,RawFileInfoData) else RawFileInfoData()
        
                
    def show(self):
        print("Artist Data Class")
        print("-------------------------")
        if self.artist.native != self.artist.name:
            print("Artist:  {0} ({1})".format(self.artist.name, self.artist.native))
        else:
            print("Artist:  {0}".format(self.artist.name))
        print("Meta:    {0}".format(self.meta.title))
        print("         {0}".format(self.meta.url))
        print("Info:    {0}".format(self.info.filename))
        print("         {0}".format(self.info.created))
        print("         {0}".format(self.info.called))
        print("URL:     {0}".format(self.url.url))
        print("ID:      {0}".format(self.ID.ID))
        print("Profile: {0}".format(self.profile.get()))
        print("Pages:   {0}".format(self.pages.get()))
        print("Media:   {0}".format(self.mediaCounts.get()))
        for mediaType,mediaTypeData in self.media.media.items():
            print("   {0}".format(mediaType))
            mediaTypeDataValues = mediaTypeData.values() if isinstance(mediaTypeData, dict) else mediaTypeData
            for mediaTypeRecord in mediaTypeDataValues:
                if isinstance(mediaTypeRecord, RawMediaReleaseData):
                    print(f"      {mediaTypeRecord.album}")
                elif isinstance(mediaTypeRecord, RawMediaMetaData):
                    print(f"      {mediaTypeRecord.name}")
                elif isinstance(mediaTypeRecord, dict):
                    print(f"      {mediaTypeRecord}")
                elif isinstance(mediaTypeRecord, str):
                    print(f"      '{mediaTypeRecord}'")
                else:
                    print(f"      [{mediaTypeRecord}] ?")
        
    def get(self):
        return self.__dict__
    
    

class RawArtistMediaData:
    def __init__(self, artist=None, ID=None, media=None, info=None, err=None):
        self.ID          = ID if isinstance(ID,RawIDData) else RawIDData()
        self.artist      = artist if isinstance(artist,RawNameData) else RawNameData()
        self.media       = media if isinstance(media,RawMediaData) else RawMediaData()
        self.info        = info if isinstance(info,RawFileInfoData) else RawFileInfoData()
        
        
    def show(self):
        print("Artist Media Data Class")
        print("-------------------------")
        print("Artist:  {0}".format(self.artist.name))
        print("Info:    {0}".format(self.info.called))
        print("ID:      {0}".format(self.ID.ID))
        for mediaType,mediaTypeData in self.media.media.items():
            print("   {0}".format(mediaType))
            mediaTypeDataValues = mediaTypeData.values() if isinstance(mediaTypeData, dict) else mediaTypeData
            for mediaTypeRecord in mediaTypeDataValues:
                if isinstance(mediaTypeRecord, RawMediaReleaseData):
                    print(f"      {mediaTypeRecord.album}")
                elif isinstance(mediaTypeRecord, RawMediaMetaData):
                    print(f"      {mediaTypeRecord.name}")
                elif isinstance(mediaTypeRecord, dict):
                    print(f"      {mediaTypeRecord}")
                elif isinstance(mediaTypeRecord, str):
                    print(f"      '{mediaTypeRecord}'")
                else:
                    print(f"      [{mediaTypeRecord}] ?")
                    
        
    def get(self):
        return self.__dict__
    
    

class RawArtistProfileData:
    def __init__(self, ID=None, profile=None, info=None, err=None):
        self.ID          = ID if isinstance(ID,RawIDData) else RawIDData()
        self.profile     = profile if isinstance(profile,RawProfileData) else RawProfileData()
        self.info        = info if isinstance(info,RawFileInfoData) else RawFileInfoData()
        
        
    def show(self):
        print("Artist Media Data Class")
        print("-------------------------")
        print("ID:      {0}".format(self.ID.ID))
        print("Info:    {0}".format(self.info.called))
        print("Profile: {0}".format(self.profile.get()))
    
    
    def get(self):
        return self.__dict__
    

class RawDataBase:
    def __init__(self):
        self.bsdata = None
        manc = MusicDBArtistName()
        self.clean = manc.clean

    ###################################################################################
    def makeRawData(self, *args, **kwargs): return RawData(*args, **kwargs)
    def isRawData(self, arg): return isinstance(arg, RawData)

    ###################################################################################
    def makeRawArtistMediaData(self, *args, **kwargs): return RawArtistMediaData(*args, **kwargs)
    def isRawArtistMediaData(self, arg): return isinstance(arg, RawArtistMediaData)

    ###################################################################################
    def makeRawArtistProfileData(self, *args, **kwargs): return RawArtistProfileData(*args, **kwargs)
    def isRawArtistProfileData(self, arg): return isinstance(arg, RawArtistProfileData)

    ###################################################################################
    def makeRawDataBase(self, *args, **kwargs): return RawDataBase(*args, **kwargs)
    def isRawDataBase(self, arg): return isinstance(arg, RawDataBase)

    ###################################################################################
    def makeRawNameData(self, *args, **kwargs): return RawNameData(*args, **kwargs)
    def isRawNameData(self, arg): return isinstance(arg, RawNameData)

    ###################################################################################
    def makeRawMetaData(self, *args, **kwargs): return RawMetaData(*args, **kwargs)
    def isRawMetaData(self, arg): return isinstance(arg, RawMetaData)

    ###################################################################################
    def makeRawIDData(self, *args, **kwargs): return RawIDData(*args, **kwargs)
    def isRawIDData(self, arg): return isinstance(arg, RawIDData)

    ###################################################################################
    def makeRawURLData(self, *args, **kwargs): return RawURLData(*args, **kwargs)
    def isRawURLData(self, arg): return isinstance(arg, RawURLData)

    ###################################################################################
    def makeRawURLInfoData(self, *args, **kwargs): return RawURLInfoData(*args, **kwargs)
    def isRawURLInfoData(self, arg): return isinstance(arg, RawURLInfoData)

    ###################################################################################
    def makeRawPageData(self, *args, **kwargs): return RawPageData(*args, **kwargs)
    def isRawPageData(self, arg): return isinstance(arg, RawPageData)

    ###################################################################################
    def makeRawProfileData(self, *args, **kwargs): return RawProfileData(*args, **kwargs)
    def isRawProfileData(self, arg): return isinstance(arg, RawProfileData)

    ###################################################################################
    def makeRawMediaData(self, *args, **kwargs): return RawMediaData(*args, **kwargs)
    def isRawMediaData(self, arg): return isinstance(arg, RawMediaData)

    ###################################################################################
    def makeRawMediaReleaseData(self, *args, **kwargs): return RawMediaReleaseData(*args, **kwargs)
    def isRawMediaReleaseData(self, arg): return isinstance(arg, RawMediaReleaseData)

    ###################################################################################
    def makeRawMediaMetaData(self, *args, **kwargs): return RawMediaMetaData(*args, **kwargs)
    def isRawMediaMetaData(self, arg): return isinstance(arg, RawMediaMetaData)

    ###################################################################################
    def makeRawMediaCollection(self, *args, **kwargs): return RawMediaCollection(*args, **kwargs)
    def isRawMediaCollection(self, arg): return isinstance(arg, RawMediaCollection)

    ###################################################################################
    def makeRawMediaAuxiliaryData(self, *args, **kwargs): return RawMediaAuxiliaryData(*args, **kwargs)
    def isRawMediaAuxiliaryData(self, arg): return isinstance(arg, makeRawMediaAuxiliaryData)

    ###################################################################################
    def makeRawMediaAlbumData(self, *args, **kwargs): return RawMediaAlbumData(*args, **kwargs)
    def isRawMediaAlbumData(self, arg): return isinstance(arg, RawMediaAlbumData)

    ###################################################################################
    def makeRawMediaCountsData(self, *args, **kwargs): return RawMediaCountsData(*args, **kwargs)
    def isRawMediaCountsData(self, arg): return isinstance(arg, RawMediaCountsData)

    ###################################################################################
    def makeRawFileInfoData(self, *args, **kwargs): return RawFileInfoData(*args, **kwargs)
    def isRawFileInfoData(self, arg): return isinstance(arg, RawFileInfoData)

    ###################################################################################
    def makeRawTextData(self, *args, **kwargs): return RawTextData(*args, **kwargs)
    def isRawTextData(self, arg): return isinstance(arg, RawTextData)

    ###################################################################################
    def makeRawLinkData(self, *args, **kwargs): return RawLinkData(*args, **kwargs)
    def isRawLinkData(self, arg): return isinstance(arg, RawLinkData)

    ###################################################################################
    def makeRawTagData(self, *args, **kwargs): return RawTagData(*args, **kwargs)
    def isRawTagData(self, arg): return isinstance(arg, RawTagData)  
    

    def getSeriesData(self, ifile):
        self.ifile  = None
        self.bsdata = ifile if isinstance(ifile,Series) else None
        
    def getDataFrameData(self, ifile):
        self.ifile  = None
        self.bsdata = ifile if isinstance(ifile,DataFrame) else None
        
    def getDictData(self, ifile):
        self.ifile  = ifile
        self.bsdata = ifile if isinstance(ifile,dict) else None
        
    def getTupleData(self, ifile):
        self.ifile  = ifile
        self.bsdata = ifile if isinstance(ifile,tuple) else None
        
    def getListData(self, ifile):
        self.ifile  = ifile
        self.bsdata = ifile if isinstance(ifile,list) else None
        
    def getPickledData(self, ifile):
        self.ifile  = ifile
        try:
            self.bsdata = FileIO().get(ifile)
        except:
            raise ValueError("Could not open data: [{0}]".format(ifile))
        
    def getPickledHTMLData(self, ifile):
        self.ifile  = ifile
        self.getPickledData(ifile)
        self.bsdata = HTMLIO().get(self.bsdata)
        
    def getPickledBytesData(self, ifile):
        self.ifile  = ifile
        self.getPickledData(ifile)
        self.bsdata = HTMLIO().get(FileIO.get(ifile))
        
    def getBytesData(self, ifile):
        self.ifile  = ifile
        self.bsdata = HTMLIO().get(ifile)
                
    def getInfo(self):
        return self.makeRawFileInfoData(self.ifile)

    def assertData(self):
        if self.bsdata is None:
            raise ValueError("There is no BS4 or DB data!")