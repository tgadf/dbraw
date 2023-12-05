from dbraw import RawDataIOBase


def test_dataio_id():
    rawio = RawDataIOBase()
    rawdata = rawio.makeRawIDData(ID="349384")
    assert rawio.isRawIDData(rawdata)

            
def test_dataio_url():
    rawio = RawDataIOBase()
    rawdata = rawio.makeRawURLData(url='http://www.something.com')
    assert rawio.isRawURLData(rawdata)

            
def test_dataio_name():
    rawio = RawDataIOBase()
    rawdata = rawio.makeRawNameData(name='My Name')
    assert rawio.isRawNameData(rawdata)

            
def test_dataio_meta():
    rawio = RawDataIOBase()
    rawdata = rawio.makeRawMetaData(title='My Title', url='http://www.something.com')
    assert rawio.isRawMetaData(rawdata)


def test_dataio_info():
    rawio = RawDataIOBase()
    rawdata = rawio.makeRawInfoData(filename="MyFile.ext")
    assert rawio.isRawInfoData(rawdata)


def test_dataio_basic():
    rawio = RawDataIOBase()
    rawid = rawio.makeRawIDData(ID="349384")
    rawurl = rawio.makeRawURLData(url='http://www.something.com')
    rawname = rawio.makeRawNameData(name='My Name')
    rawdata = rawio.makeRawBasicData(ID=rawid, url=rawurl, name=rawname)
    assert rawio.isRawBasicData(rawdata)


def test_dataio_profile():
    rawio = RawDataIOBase()
    rawdata = rawio.makeRawProfileData(general={}, genres={}, tags={}, external={}, extra={})
    assert rawio.isRawProfileData(rawdata)
    

def test_dataio_artist():
    rawio = RawDataIOBase()
    rawid = rawio.makeRawIDData(ID="349384")
    rawurl = rawio.makeRawURLData(url='http://www.something.com')
    rawname = rawio.makeRawNameData(name='My Name')
    rawbasic = rawio.makeRawBasicData(ID=rawid, url=rawurl, name=rawname)
    rawinfo = rawio.makeRawInfoData(filename="MyFile.ext")
    rawmeta = rawio.makeRawMetaData(title='My Title', url='http://www.something.com')
    rawprofile = rawio.makeRawProfileData(general={}, genres={}, tags={}, external={}, extra={})
    
    mediaCollection = {}
    
    mediaTypeName = "Album"
    artistID = '12345'
    albumID = '56789'
    name = "My Album"
    pdbid = "-".join([mediaTypeName, f"Art{artistID}", f"Alb{albumID}"])
    mediaRootData = rawio.makeRawMediaRootData(pdbid=pdbid, dbid=albumID, name=name)
    
    if mediaCollection.get(mediaTypeName) is None:
        mediaCollection[mediaTypeName] = []
    mediaCollection[mediaTypeName].append(mediaRootData)
            
    rawmedia = rawio.makeRawMediaCollectionData()
    for mediaTypeName, mediaTypeData in mediaCollection.items():
        rawmedia.add(mediaTypeName, mediaTypeData)
    
    rawdata = rawio.makeRawArtistData(basic=rawbasic, profile=rawprofile,
                                      media=rawmedia, info=rawinfo, meta=rawmeta)
    assert rawio.isRawArtistData(rawdata)
    

if __name__ == "__main__":
    test_dataio_id()
    test_dataio_url()
    test_dataio_name()
    test_dataio_meta()
    test_dataio_info()
    test_dataio_basic()
    test_dataio_profile()
    test_dataio_artist()
    