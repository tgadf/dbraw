""" Store Data Class """

__all__ = ["StoreData"]

from master import MasterParams, MasterDBs, MasterPaths, MasterMetas, MasterBasic
from gate import IOStore
from timeutils import Timestat
from ioutils import HTMLIO, FileIO
from fileutils import FileInfo, DirInfo
from pandas import DataFrame, Series, concat
from time import sleep

class StoreData:
    def __init__(self, db, dType):
        self.hio = HTMLIO()
        self.io  = FileIO()
        mp     = MasterParams(verbose=True)
        self.dbs    = mp.getDBs()
        self.ios    = IOStore()
        self.db     = db
        self.dType  = dType
        self.mdbio  = self.ios.get(db)
        self.dTypes = {"Genius": "Song", "Discogs": "Master", "Deezer": "Album", "AllMusic": "Credit", "Spotify": "Album", "JioSaavn": "Album",
                       "Beatport": "Artist", "MetalArchives": "Artist", "MyMixTapez": "Artist", "RateYourMusic": "Artist",
                       "AlbumOfTheYear": "Album", "YouTubeMusic": "Artist", "AppleMusic": "Artist", "LastFM": "Artist", "Wikidata": "Artist",
                       "Soundcloud": "Artist", "Bandcamp": "Artist", "SetListFM": "Artist", "SpiritOfMetal": "Artist", "RollDaBeats": "Artist"}
        
        
        
        
    ###############################################################################################################################################
    ## Mod/Glob Values Lookups
    ###############################################################################################################################################
    def getModGlobVal(self, modVal):
        retval = f"0{modVal}" if modVal < 10 else f"{modVal}"
        return retval
    
    
    
    def getModValues(self, mdbioGlobal, localDataID):
        if mdbioGlobal.db in ["Traxsource"]:
            localDataIDTrax = localDataID.split('-')[0] if self.dType == "Extra" else localDataID
            modVal  = self.getModGlobVal(int(mdbioGlobal.getModVal(localDataIDTrax)))
            globVal = self.getModGlobVal(int(mdbioGlobal.mv.getGlobVal(localDataIDTrax)))
        elif mdbioGlobal.db in ["JioSaavn"]:
            modVal  = self.getModGlobVal(int(mdbioGlobal.getModVal(localDataID)))
            globVal = self.getModGlobVal(int(mdbioGlobal.mv.getGlobVal(localDataID)))
        elif hasattr(mdbioGlobal, "getGlobVal") and callable(getattr(mdbioGlobal, "getGlobVal")):
            modVal  = self.getModGlobVal(int(mdbioGlobal.getModVal(localDataID)))
            globVal = self.getModGlobVal(int(mdbioGlobal.getGlobVal(localDataID)))
        else:
            modVal  = self.getModGlobVal(int(mdbioGlobal.mv.getModVal(localDataID)))
            globVal = self.getModGlobVal(int(mdbioGlobal.mv.getGlobVal(localDataID)))
            if False:
                if len(localDataID) == 1:
                    modVal  = self.getModGlobVal(int(localDataID[0]))
                    globVal = self.getModGlobVal(0)
                elif len(localDataID) == 2:
                    modVal  = self.getModGlobVal(int(localDataID[-2:]))
                    globVal = self.getModGlobVal(0)
                elif len(localDataID) == 3:
                    modVal  = self.getModGlobVal(int(localDataID[-2:]))
                    globVal = self.getModGlobVal(int(localDataID[-3:-2]))
                else:
                    modVal  = self.getModGlobVal(int(localDataID[-2:]))
                    globVal = self.getModGlobVal(int(localDataID[-4:-2]))
        return modVal,globVal
    
    
    
    ###############################################################################################################################################
    ## File IO / Artist ID
    ###############################################################################################################################################
    def getRawData(self, finfo):
        try:
            localData = self.io.get(finfo)
        except:
            print(f"Error with {finfo.str}")
            localData = None
        return localData

    
    def getDBID(self, db, localData, finfo):
        localDataID = None
        if db in ["Deezer", "Discogs", "Genius", "MetalArchives"]:
            key = 'id'
            if db == "Genius" and self.dType == "ArtistSong":
                key = 'artistID'
            if db == "Deezer" and self.dType == "ArtistRelated":
                key = 'ArtistID'
            localDataID = localData.get(key) if isinstance(localData,dict) else None
            if localDataID is None:
                return None
                print(f"Error with {db} ID")
                localDataID = None
            elif isinstance(localDataID,int):
                localDataID = str(localDataID)                
            if localDataID is not None and not isinstance(localDataID,str):
                print(f"Error with {db} ID {localDataID} is not a string")
                localDataID = None
        elif db in ["Traxsource"]:
            localDataID = finfo.basename
        elif db in ["AllMusic", "Spotify", "AlbumOfTheYear", "JioSaavn", "Beatport", "YouTubeMusic", "Napster", "MyMixTapez",
                    "LastFM", "AppleMusic", "Wikidata", "Soundcloud", "Bandcamp", "SetListFM", "SpiritOfMetal", "RollDaBeats"]:
            localDataID = finfo.basename
        else:
            raise ValueError(f"Did not recognize DB {db}")

        return localDataID

    
    
    ###############################################################################################################################################
    ## Merge Local Data
    ###############################################################################################################################################
    def mergeLocalData(self, test=False, modVals=None):        
        modValsList = MasterBasic().getModVals(listIt=True) if modVals is None else modVals
        mdbioLocal  = self.ios.get(self.db, local=True, mkDirs=False)
        dstDir      = DirInfo(mdbioLocal.dir.getRawDataDir())
        prevDir     = DirInfo(mdbioLocal.dir.getRawDataDir().join("prev"))
        prevDir.mkDir()
        
        ts = Timestat("Creating ModVal Files")
        modVals  = {mVal: self.getModGlobVal(mVal) for mVal in range(1)} if test is True else {mVal: self.getModGlobVal(mVal) for mVal in modValsList}
        globVals = {gVal: self.getModGlobVal(gVal) for gVal in modValsList}

        globValData = {}
        for n,(modVal,modGlobVal) in enumerate(modVals.items()):
            srcDir  = eval(f"mdbioLocal.dir.getRaw{self.dType}ModValDataDir(modVal)")

            print(f"src={srcDir.str}    ", end="")
            files = [FileInfo(ifile) for ifile in srcDir.glob("*.p", debug=False)]
            print(f"ModVal={modGlobVal}    Files={len(files)}    ", end="")
            for finfo in files:
                localData = self.getRawData(finfo)        
                if localData is None:
                    continue

                localDataID = self.getDBID(self.db, localData, finfo)
                if localDataID is None:
                    continue

                try:
                    localModVal,globVal   = self.getModValues(mdbioLocal, localDataID)
                except:
                    raise ValueError(f"{finfo.str}   {db}.  {localDataID}")

                if globValData.get(localModVal) is None:
                    globValData[localModVal] = {}
                if globValData[localModVal].get(globVal) is None:
                    globValData[localModVal][globVal] = {}
                globValData[localModVal][globVal][localDataID] = localData

            numMod   = len(globValData)
            numGlobs = sum([len(gData) for gData in globValData.values()])
            print(f"NumMod={numMod}    NumGlobs={numGlobs}")
    
    
        if test is False:
            ts = Timestat("Saving ModVal Data")
            for n,modGlobVal in enumerate(globValData.keys()):
                modValData = globValData[modGlobVal]
                for g,(globVal,retval) in enumerate(modValData.items()):
                    if len(retval) > 0:
                        savename = dstDir.join(f"{self.db}-{self.dType}-mv-{modGlobVal}-gv-{globVal}.p")
                        if savename.exists():
                            oldData = self.io.get(savename)
                            retval.update(oldData)
                    if g % 25 == 0: print(f"ModVal={modGlobVal}   GlobVal={globVal}    Data={len(retval)}     Saved={savename.str}")
                    self.io.save(idata=retval, ifile=savename)
                if (n+1) % 5 == 0:
                    ts.update(n=n+1,N=100)
                    
            ts.stop()
            
            
    ###############################################################################################################################################
    ## Merge With Destination Data
    ###############################################################################################################################################
    def makeDestination(self):
        mdbioGlobal = self.ios.get(self.db, local=False, mkDirs=True)
        for modVal in range(100):
            dstDir  = eval(f"mdbioGlobal.dir.getRaw{self.dType}ModValDataDir(modVal)")
            dstDir.mkDir()
            
            
    def mergeGlobalData(self, test=False):
        mdbioGlobal = self.ios.get(self.db, local=False, mkDirs=False)
        mdbioLocal  = self.ios.get(self.db, local=True,  mkDirs=False)
        prevDir     = DirInfo(mdbioLocal.dir.getRawDataDir().join("prev"))
        prevDir.mkDir()
        srcDir      = DirInfo(mdbioLocal.dir.getRawDataDir())


        ts = Timestat("Merging Local With Global")
        numModVals = 1 if test is True else 100
        modVals  = {mVal: self.getModGlobVal(mVal) for mVal in range(numModVals)}
        for n,(modVal,modGlobVal) in enumerate(modVals.items()):
            if (n+1) % 5 == 0:
                ts.update(n=n+1,N=100)            
            dstDir  = eval(f"mdbioGlobal.dir.getRaw{self.dType}ModValDataDir(modVal)")
            globCmd = srcDir.glob(f"{self.db}-{self.dType}-mv-{modGlobVal}-gv-*.p", debug=False)
            files = [FileInfo(ifile) for ifile in globCmd]
            if test is True:
                print(len(files))
            for g,finfo in enumerate(files):
                if g % 25 == 0: print(f"File={finfo.name}   ", end="")
                dstFile = dstDir.join(finfo.name)
                if test is True:
                    print(finfo.path)
                    print(dstFile.path)
                    print(dstFile.exists())

                if dstFile.exists():
                    localData = self.io.get(finfo)
                    if g % 25 == 0: print(f"Local={len(localData)}    ", end="")
                    globalData = self.io.get(dstFile)
                    globalData = {} if globalData is None else globalData
                    if g % 25 == 0: print(f"Global={len(globalData)}    ", end="")
                    globalData.update(localData)
                    if g % 25 == 0: print(f"Total={len(globalData)}    ", end="")
                    if test is True:
                        break
                    self.io.save(idata=globalData, ifile=dstFile)
                    prevFile = prevDir.join(finfo.name)
                    finfo.mvFile(prevFile, debug=False)
                    if g % 25 == 0: print(f"File={dstFile.str}")
                else:
                    if test is True:
                        break
                    finfo.mvFile(dstFile, debug=False)
                    if g % 25 == 0: print(f"File={dstFile.str}")

                if test is True:
                    break
                sleep(0.5)
            if test is True:
                break
                
        ts.stop()