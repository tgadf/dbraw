""" Raw Data Media Base Classes """

__all__ = ["RawMediaCollectionData", "RawMediaRootData", "RawMediaDeepData"]

from pandas import concat, DataFrame, Series
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
            return isinstance(mediaData, (RawMediaRootData, RawMediaDeepData))
        
        allowDuplicates = allowDuplicates if isinstance(allowDuplicates, bool) else self.allowDuplicates
        assert isinstance(mediaType, str), f"MediaType [{mediaType}] is not a string"
        mediaTypeData = [mediaTypeData] if isMedia(mediaTypeData) else mediaTypeData
        assert isinstance(mediaTypeData, list), f"MediaTypeData [{mediaTypeData}] is not a list"
        
        mediaElementData = {}
        for mediaTypeRecord in mediaTypeData:
            assert isMedia(mediaTypeRecord), f"Could not add mediaTypeRecord of type [{type(mediaTypeRecord)}]"
            key = mediaTypeRecord.pdbid
            value = {k: v for k, v in mediaTypeRecord.get().items() if k not in ["pdbid"]}
            value["Type"] = mediaType
            mediaElementData[key] = value
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
        
    def merge(self, collectionData, allowDuplicates=None, **kwargs) -> 'None':
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


class RawMediaDataBase:
    def __init__(self, pdbid, dbid):
        assert isinstance(pdbid, str), f"PanDB ID [{pdbid}] is not correctly formatted"
        assert isinstance(dbid, str), f"DB ID [{dbid}] is not correctly formatted"
        setattr(self, 'pdbid', pdbid)
        setattr(self, 'dbid', dbid)
        
    def get(self):
        return self.__dict__
    
    def __eq__(self, rootData):
        retval = rootData.__dict__ == self.__dict__ if hasattr(rootData, "__dict__") else None
        return retval

    def compare(self, rootData, keys=None):
        assert hasattr(rootData, "__dict__"), f"rootData [{rootData}] does not have a dictionary"
        if isinstance(keys, list):
            selfData = {k: v for k, v in self.__dict__.items() if k in keys}
            rootData = {k: v for k, v in rootData.__dict__.items() if k in keys}
            return selfData == rootData
        return self == rootData
        
    
class RawMediaRootData(RawMediaDataBase):
    def __repr__(self):
        return f"RawMediaRootData(pdbid={self.pdbid}, dbid={self.dbid}, name={self.name})"
    
    def __init__(self, pdbid, dbid, name):
        super().__init__(pdbid, dbid)
        assert isinstance(name, str), f"Media Name [{name}] is not correctly formatted"
        setattr(self, 'name', name)
        

class RawMediaDeepData(RawMediaDataBase):
    def __repr__(self):
        return f"RawMediaDeepData(pdbid={self.pdbid}, dbid={self.dbid}, artids={self.artids})"
    
    def __init__(self, pdbid, dbid, artids, **kwargs):
        super().__init__(pdbid, dbid)
        assert isinstance(artids, list), f"Artist IDs [{artids}] is not correctly formatted"
        assert all([isinstance(artid, str) for artid in artids]), f"artids [{artids}] are not all str"
        setattr(self, 'artids', artids)
        for key, value in kwargs.items():
            setattr(self, key, value)
            