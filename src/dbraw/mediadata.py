""" Raw Data Media Base Classes """

__all__ = ["RawMediaCollectionData", "RawMediaDataBase", "RawMediaRootData", "RawMediaDeepData"]

from pandas import concat, DataFrame, Series
from utils import FileIO
from .base import RawBaseData


###########################################################################
# Primary Artist Media Collection Class
###########################################################################
class RawMediaCollectionData(RawBaseData):
    def __repr__(self):
        return "RawMediaCollectionData(allowDuplicates={self.allowDuplicates})"
    
    def __init__(self, allowDuplicates=False) -> 'None':
        self.collection = DataFrame()
        self.allowDuplicates = allowDuplicates
        
    def add(self, mediaType, mediaTypeData, allowDuplicates=None) -> 'None':
        def isMedia(mediaData):
            return isinstance(mediaData, (RawMediaDataBase, RawMediaRootData, RawMediaDeepData))
        
        allowDuplicates = allowDuplicates if isinstance(allowDuplicates, bool) else self.allowDuplicates
        assert isinstance(mediaType, str), f"MediaType [{mediaType}] is not a string"
        mediaTypeData = [mediaTypeData] if isMedia(mediaTypeData) else mediaTypeData
        assert isinstance(mediaTypeData, list), f"MediaTypeData [{mediaTypeData}] is not a list"
        
        mediaElementData = {}
        for mediaIDData in mediaTypeData:
            assert isMedia(mediaIDData), f"Could not add MediaIDData of type [{type(mediaIDData)}]"
            key = mediaIDData.mediaID
            value = {k: v for k, v in mediaIDData.get().items() if k not in ["mediaID"]}
            value["Type"] = mediaType
            mediaElementData[key] = value
        #if len(mediaElementData) > 0:
        #    io = FileIO()
        #    io.save(idata=mediaElementData, ifile="/Users/tgadfort/code/musicdb/ddata.p")
        #    1/0
        #print(mediaElementData)
        #mediaElementData = Series(mediaElementData).apply(Series)
        mediaElementData = DataFrame(mediaElementData).T
            
        indexIntersection = mediaElementData.index.intersection(self.collection.index)
        if len(indexIntersection) > 0 and allowDuplicates is False:
            print(f"Attempting to add media [{indexIntersection}], but these indices already exists in the collection")
            print("============== Existing Data ==============")
            print(self.collection.loc[indexIntersection].to_string())
            print("============== New Data ==============")
            print(mediaElementData.loc[indexIntersection].to_string())
            raise ValueError(f"Attempting to add media [{indexIntersection}], but these indices already exists in the collection")
            
        self.collection = concat([self.collection, mediaElementData])
        self.collection = self.collection[~self.collection.index.duplicated()]
        
    def merge(self, collectionData, allowDuplicates=None):
        allowDuplicates = allowDuplicates if isinstance(allowDuplicates, bool) else self.allowDuplicates
        assert isinstance(collectionData, RawMediaCollectionData), f"CollectionData is type [{type(collectionData)}] and not [RawMediaCollectionData] in RawMediaCollectionData.merge"
        mediaElementData = collectionData.get()
        indexIntersection = mediaElementData.index.intersection(self.collection.index)
        if len(indexIntersection) > 0 and allowDuplicates is False:
            print(f"Attempting to add media [{indexIntersection}], but these indices already exists in the collection")
            print("============== Existing Data ==============")
            print(self.collection.loc[indexIntersection].to_string())
            print("============== New Data ==============")
            print(mediaElementData.loc[indexIntersection].to_string())
            raise ValueError(f"Attempting to add media [{indexIntersection}], but these indices already exists in the collection")
            
        self.collection = concat([self.collection, mediaElementData])
        self.collection = self.collection[~self.collection.index.duplicated()]
            
    def get(self):
        return self.collection
            
    def getMedia(self):
        if isinstance(self.collection, DataFrame) and self.collection.shape[0] > 0:
            retval = {mediaType: mediaTypeData for mediaType, mediaTypeData in self.collection.groupby("Type")}
        else:
            retval = {}
        return retval
    
    def summary(self):
        print("Media")
        for mediaType, mediaTypeData in self.getMedia().items():
            names = mediaTypeData["name"] if "name" in mediaTypeData.columns else None
            nameStr = None
            if isinstance(names, Series):
                names = names[names.notna()]
                if len(names) >= 4:
                    nameStr = f"{names.iloc[0]} , {names.iloc[1]} , ... , {names.iloc[-1]}"
                elif len(names) == 3:
                    nameStr = f"{names.iloc[0]} , {names.iloc[1]} , {names.iloc[-1]}"
                elif len(names) >= 1:
                    nameStr = " , ".join(names.values)
                
            if isinstance(nameStr, str):
                print(f"{mediaType: >15}: {mediaTypeData.shape[0]: <5} | {nameStr}")
            else:
                print(f"{mediaType: >15}: {mediaTypeData.shape[0]}")

        
class RawMediaDataBase(RawBaseData):
    def __repr__(self):
        return f"RawMediaDataBase(mediaID={self.mediaID})"
    
    def __init__(self, mediaID):
        assert isinstance(mediaID, (str, tuple)), f"Media ID [{mediaID}] is not correctly formatted in RawMediaBaseData"
        self.mediaID = mediaID


class RawMediaRootData(RawMediaDataBase):
    def __repr__(self):
        return f"RawMediaRootData(mediaID={self.mediaID}, name={self.name})"
    
    def __init__(self, mediaID, name):
        super().__init__(mediaID)
        assert isinstance(name, str), f"Media Name [{name}] is not correctly formatted in RawMediaBaseData"
        self.name = name
            
    def compare(self, rootData):
        retval = rootData.__dict__ == self.__dict__ if isinstance(rootData, RawMediaRootData) else None
        return retval


class RawMediaDeepData(RawMediaDataBase):
    def __repr__(self):
        return f"RawMediaDeepData({self.__dict__})"
    
    def __init__(self, mediaID, **kwargs):
        super().__init__(mediaID)
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def compare(self, deepData):
        retval = deepData.__dict__ == self.__dict__ if isinstance(deepData, RawMediaDeepData) else None
        return retval