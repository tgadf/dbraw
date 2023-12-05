""" IO For Raw Data Classes """

__all__ = ["RawDataIOBase", "RawDataFileIO"]

from utils import FileInfo, HTMLIO, FileIO
from bs4.element import Tag
from .artistdata import RawArtistData
from .artistdata import RawBasicData, RawProfileData, RawMetaData, RawInfoData
from .artistdata import RawPageData, RawNameData, RawURLData, RawIDData
from .mediadata import RawMediaCollectionData, RawMediaRootData, RawMediaDeepData


class RawDataFileIO:
    def __init__(self, fID: str, fData, ifile: str):
        self.fid = fID
        self.ifile = ifile
        assert fData is not None, f"Data is None in RawDataFileIO. ID={fID} / ifile={ifile}"
        if isinstance(fData, str) and len(fData) < 10:
            raise TypeError(f"Data with key [{fID}] and ifile [{ifile}] is not a path and not HTML")
        if isinstance(fData, bytes) or (isinstance(fData, str) and "html" in fData):
            try:
                self.bsdata = HTMLIO().get(fData)
            except Exception as error:
                raise TypeError(f"Could not create BS4 data from bytes data: [{error}]")
        elif isinstance(fData, FileInfo) or (isinstance(fData, str) and "html" not in fData):
            try:
                self.bsdata = FileIO().get(fData)
            except Exception as error:
                raise TypeError(f"Could load data from file: [{error}]")
        else:
            self.bsdata = fData
            
    def getID(self):
        return self.fid
    
    def getFile(self):
        return self.ifile
            
    def getData(self):
        return self.bsdata
    
    
class RawDataIOBase:
    def __init__(self, verbose=False):
        self.verbose = verbose
        
    def getData(self, fID, fData, ifile):
        self.rdfio = RawDataFileIO(fID, fData, ifile)
        return self.rdfio.getData()
    
    def assertIDMatch(self, ID):
        assert ID == self.rdfio.getID(), f"Parsed RawData ID [{ID}] does not match File Key ID [{self.rdfio.getID()}] and File [{self.rdfio.getFile()}]"
        
    def getFileID(self):
        return self.rdfio.getID()
        
    def getFileInfo(self):
        return self.makeRawInfoData(self.rdfio.getFile())

    ###################################################################################
    # Artist Data
    ###################################################################################
    def makeRawArtistData(self, *args, **kwargs): return RawArtistData(*args, **kwargs)
    def isRawArtistData(self, arg): return isinstance(arg, RawArtistData)
    
    
    ###################################################################################
    # Artist Data Inputs
    ###################################################################################
    def makeRawBasicData(self, *args, **kwargs): return RawBasicData(*args, **kwargs)
    def isRawBasicData(self, arg): return isinstance(arg, RawBasicData)

    def makeRawProfileData(self, *args, **kwargs): return RawProfileData(*args, **kwargs)
    def isRawProfileData(self, arg): return isinstance(arg, RawProfileData)

    def makeRawMediaCollectionData(self, *args, **kwargs): return RawMediaCollectionData(*args, **kwargs)
    def isRawMediaCollectionData(self, arg): return isinstance(arg, RawMediaCollectionData)
    
    def makeRawMetaData(self, *args, **kwargs): return RawMetaData(*args, **kwargs)
    def isRawMetaData(self, arg): return isinstance(arg, RawMetaData)
    
    def makeRawPageData(self, *args, **kwargs): return RawPageData(*args, **kwargs)
    def isRawPageData(self, arg): return isinstance(arg, RawPageData)
    
    def makeRawInfoData(self, *args, **kwargs): return RawInfoData(*args, **kwargs)
    def isRawInfoData(self, arg): return isinstance(arg, RawInfoData)
        

    ###################################################################################
    # Artist Basic Inputs
    ###################################################################################
    def makeRawNameData(self, *args, **kwargs): return RawNameData(*args, **kwargs)
    def isRawNameData(self, arg): return isinstance(arg, RawNameData)

    def makeRawURLData(self, *args, **kwargs): return RawURLData(*args, **kwargs)
    def isRawURLData(self, arg): return isinstance(arg, RawURLData)

    def makeRawIDData(self, *args, **kwargs): return RawIDData(*args, **kwargs)
    def isRawIDData(self, arg): return isinstance(arg, RawIDData)
        

    ###################################################################################
    # Artist Media Inputs
    ###################################################################################
    def makeRawMediaDataBase(self, *args, **kwargs): return RawMediaDataBase(*args, **kwargs)
    def isRawMediaDataBase(self, arg): return isinstance(arg, RawMediaDataBase)

    def makeRawMediaRootData(self, *args, **kwargs): return RawMediaRootData(*args, **kwargs)
    def isRawMediaRootData(self, arg): return isinstance(arg, RawMediaRootData)

    def makeRawMediaDeepData(self, *args, **kwargs): return RawMediaDeepData(*args, **kwargs)
    def isRawMediaDeepData(self, arg): return isinstance(arg, RawMediaDeepData)
        

    ###################################################################################
    # Helper Functions
    ###################################################################################
    def getTextData(self, tag):
        retval = tag.text.strip() if isinstance(tag,Tag) else None
        return retval
        
    def getLinkData(self, link):
        retval = {"Attrs": link.attrs, "Text": self.getTextData(link)} if isinstance(link, Tag) else {"URL": None, "Title": None, "Text": None}
        return retval
    