from dbraw import RawDataIOBasedef test_media():    rawio = RawDataIOBase()    mediaCollection = {}    shuffleData = {}        mediaTypeName = "Album"    mediaID = "artistID123-albumID123"    title = "My Album"        mediaRootData = rawio.makeRawMediaRootData(mediaID=mediaID, name=title)        artist = "My Artist"    url = "http://www.myurl.com"    year = "1979"    mediaDeepData = rawio.makeRawMediaDeepData(mediaID=mediaID, name=title,                                               artist=artist, url=url,                                               group=mediaTypeName, year=year)                if mediaCollection.get(mediaTypeName) is None:        mediaCollection[mediaTypeName] = []    mediaCollection[mediaTypeName].append(mediaRootData)    shuffleData[mediaID] = mediaDeepData                mediaData = rawio.makeRawMediaCollectionData()    for mediaTypeName, mediaTypeData in mediaCollection.items():        mediaData.add(mediaTypeName, mediaTypeData)                if __name__ == "__main__":    test_media()