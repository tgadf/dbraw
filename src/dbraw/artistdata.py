""" Raw Artist Data Base Classes """

__all__ = ["RawBaseData", "RawIDData", "RawURLData", "RawNameData",
           "RawMetaData", "RawPageData", "RawInfoData", "RawBasicData",
           "RawProfileData", "RawArtistData"]

from utils import FileInfo
from numpy import ceil
from datetime import datetime
from .base import RawBaseData
from .mediadata import RawMediaCollectionData
        
        
###################################################
# Primary Artist ID Class
###################################################
class RawIDData(RawBaseData):
    def __repr__(self):
        return f"RawIDData(id={self.id})"
    
    def __init__(self, ID: str, err=None):
        assert isinstance(ID, str), f"ID [{ID}] is not a string in RawIDData"
        self.id = ID
        
        
###################################################
# Primary Artist URL Class
###################################################
class RawURLData(RawBaseData):
    def __repr__(self):
        return f"RawURLData(url={self.url})"
    
    def __init__(self, url: str, err=None):
        assert isinstance(url, str), f"URL [{url}] is not a string in RawURLData"
        self.url = url
        
        
###################################################
# Primary Artist Name Class
###################################################
class RawNameData(RawBaseData):
    def __repr__(self):
        return f"RawNameData(name={self.name})"
    
    def __init__(self, name: str, native=None, err=None):
        assert isinstance(name, str), f"Name [{name}] is not a string in RawNameData"
        self.name = name
        self.natve = native if isinstance(native, str) is None else name
        
        
###################################################
# Primary Site MetaData Class
###################################################
class RawMetaData(RawBaseData):
    def __repr__(self):
        return f"RawMetaData(title={self.title}, url={self.url})"
    
    def __init__(self, title: str, url: str, err=None):
        assert isinstance(title, str), f"Title [{title}] is not a string in RawMetaData"
        self.title = title
        assert isinstance(url, str), f"URL [{url}] is not a string in RawMetaData"
        self.url = url


###################################################
# Primary Site Pagination Class
###################################################
class RawPageData(RawBaseData):
    def __repr__(self):
        return f"RawPageData(ppp={self.ppp}, tot={self.tot}, more={self.more}, redo={self.redo})"
    
    def __init__(self, ppp=None, tot=None, more=None, redo=None, err=None):
        assert isinstance(ppp, int) or ppp is None, f"ppp [{ppp}] is not an int or None in RawPageData"
        self.ppp = ppp
        assert isinstance(tot, int) or tot is None, f"tot [{ppp}] is not an int or None in RawPageData"
        self.tot = tot
        self.pages = int(ceil(tot / ppp)) if (isinstance(ppp, int) and isinstance(tot, int)) else None
        assert isinstance(more, bool) or more is None, f"More [{more}] is not a bool or None in RawPageData"
        self.more = more
        assert isinstance(redo, bool) or more is None, f"Redo [{redo}] is not a bool or None in RawPageData"
        self.redo = redo
        
        
###################################################
# Filename/Site MetaData Class
###################################################
class RawInfoData(RawBaseData):
    def __repr__(self):
        return f"RawInfoData(filename={self.filename})"
    
    def __init__(self, filename: str):
        self.called = datetime.now()
        self.filename = filename
        self.created = filename.time() if isinstance(filename, FileInfo) else None
        
        
###################################################
# Primary Artist Basic Data Class
###################################################
class RawBasicData(RawBaseData):
    def __repr__(self):
        return f"RawBasicData(name={self.name}, id={self.id}, url={self.url})"
    
    def __init__(self, name, url, ID, err=None):
        assert isinstance(name, RawNameData), f"Name [{name}] is not a string in RawNameData"
        self.name = getattr(name, 'name')
        assert isinstance(url, RawURLData), f"URL [{url}] is not a string in RawURLData"
        self.url = getattr(url, 'url')
        assert isinstance(ID, RawIDData), f"ID [{ID}] is not a string in RawIDData"
        self.id = getattr(ID, 'id')
    
    def summary(self):
        print("Basic")
        for key, value in self.get().items():
            print(f"{key.title(): >15}: {value}")
        

###################################################
# Primary Artist Profile Class
###################################################
class RawProfileData(RawBaseData):
    def __repr__(self):
        return f"RawProfileData(general={self.general}, genres={self.genres}, tags={self.tags}, external={self.external}, extra={self.extra})"
    
    def __init__(self, general=None, genres=None, tags=None, external=None, extra=None, err=None):
        assert isinstance(general, dict) or general is None, f"general [{general}] is not a dict or None in RawProfileData"
        self.general = general
        assert isinstance(genres, (list, dict)) or genres is None, f"genres [{genres}] is not a list/dict or None in RawProfileData"
        self.genres = genres
        assert isinstance(tags, (list, dict)) or tags is None, f"tags [{tags}] is not a list/dict or None in RawProfileData"
        self.tags = tags
        assert isinstance(external, dict) or external is None, f"external [{external}] is not a dict or None in RawProfileData"
        self.external = external
        assert isinstance(extra, dict) or extra is None, f"extra [{extra}] is not a dict or None in RawProfileData"
        self.extra = extra
        
    def merge(self, profileData):
        assert isinstance(profileData, RawProfileData), f"ProfileData is type [{type(profileData)}] and not [RawProfileData] in RawProfileData.merge"
        for group, groupData in profileData.get().items():
            self.mergeData(group, groupData)
            
    def summary(self):
        print("Profile")
        for key, value in self.get().items():
            print(f"{key.title(): >15}: {value}")
            

###########################################################################
# Raw Artist Data Container
###########################################################################
class RawArtistData:
    def __init__(self, **kwargs):
        dTypes = {"basic": RawBasicData, "profile": RawProfileData, "media": RawMediaCollectionData,
                  "meta": RawMetaData, "pages": RawPageData, "info": RawInfoData}
        self.show = self.summary
        for key, dType in dTypes.items():
            value = kwargs.get(key)
            assert isinstance(value, dType) or value is None
            if isinstance(value, dType):
                setattr(self, key, value)
                
    ###########################################################################
    # Merge I/O
    ###########################################################################
    def mergeAttr(self, key, attrData, **kwargs):
        if key not in ["media", "profile"]:
            raise ValueError("MergeAttr key must be either media or profile")
        if any([key == "media" and not isinstance(attrData, RawMediaCollectionData), key == "profile" and not isinstance(attrData, RawProfileData)]):
            return
        if hasattr(self, key):
            getattr(self, key).merge(attrData, **kwargs)
        else:
            setattr(self, key, attrData)
        
    def mergeMedia(self, mediaData, **kwargs):
        if isinstance(mediaData, RawMediaCollectionData):
            self.mergeAttr("media", mediaData, **kwargs)
            
    def mergeProfile(self, profileData, **kwargs):
        if isinstance(profileData, RawProfileData):
            self.mergeAttr("profile", profileData, **kwargs)
             
    ###########################################################################
    # Merge
    ###########################################################################
    def merge(self, mergeData, **kwargs):
        if isinstance(mergeData, RawArtistData):
            self.mergeMedia(getattr(mergeData, "media"), **kwargs)
            self.mergeProfile(getattr(mergeData, "profile"), **kwargs)
        elif isinstance(mergeData, RawMediaCollectionData):
            self.mergeMedia(mergeData, **kwargs)
        elif isinstance(mergeData, RawProfileData):
            self.mergeProfile(mergeData, **kwargs)
        else:
            raise TypeError(f"MergeData is type [{type(mergeData)}] and not allowed in RawArtistData.merge")
        
    ###########################################################################
    # Summary
    ###########################################################################
    def summary(self):
        attrData = {attr: getattr(self, attr) for attr in ["basic", "profile", "media"] if hasattr(self, attr)}
        for attr, attrValue in attrData.items():
            if hasattr(attrValue, "summary") and callable(getattr(attrValue, "summary")):
                attrValue.summary()
            
            
            