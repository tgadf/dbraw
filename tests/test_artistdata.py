from dbraw import RawIDData
from dbraw import RawURLData
from dbraw import RawNameData
from dbraw import RawMetaData
from dbraw import RawInfoData
from dbraw import RawBasicData
from dbraw import RawProfileData


def test_rawid():
    rawid = RawIDData(ID='3494')
    assert hasattr(rawid, 'id'), f"rawid {rawid} does not have id"


def test_rawurl():
    rawurl = RawURLData(url='http://www.something.com')
    assert hasattr(rawurl, 'url'), f"rawurl {rawurl} does not have url"


def test_rawname():
    rawname = RawNameData(name='My Name')
    assert hasattr(rawname, 'name'), f"rawname {rawname} does not have name"


def test_rawmeta():
    rawmeta = RawMetaData(title='My Title', url='http://www.something.com')
    assert hasattr(rawmeta, 'title'), f"rawmeta {rawmeta} does not have title"
    assert hasattr(rawmeta, 'url'), f"rawmeta {rawmeta} does not have url"


def test_rawinfo():
    rawinfo = RawInfoData(filename="MyFile.ext")
    assert hasattr(rawinfo, 'filename'), f"rawinfo {rawinfo} does not have filename"
    assert hasattr(rawinfo, 'called'), f"rawinfo {rawinfo} does not have called"
    assert hasattr(rawinfo, 'created'), f"rawinfo {rawinfo} does not have created"


def test_rawbasic():
    rawid = RawIDData(ID='3494')
    rawurl = RawURLData(url='http://www.something.com')
    rawname = RawNameData(name='My Name')
    rawbasic = RawBasicData(ID=rawid, url=rawurl, name=rawname)
    assert hasattr(rawbasic, 'id'), f"rawbasic {rawbasic} does not have id"
    assert hasattr(rawbasic, 'url'), f"rawbasic {rawbasic} does not have url"
    assert hasattr(rawbasic, 'name'), f"rawbasic {rawbasic} does not have name"


def test_rawprofile():
    rawprofile = RawProfileData(general={}, genres={}, tags={}, external={}, extra={})
    assert hasattr(rawprofile, 'general'), f"rawprofile {rawprofile} does not have general"
    assert hasattr(rawprofile, 'genres'), f"rawprofile {rawprofile} does not have genres"
    assert hasattr(rawprofile, 'tags'), f"rawprofile {rawprofile} does not have tags"
    assert hasattr(rawprofile, 'external'), f"rawprofile {rawprofile} does not have external"
    assert hasattr(rawprofile, 'extra'), f"rawprofile {rawprofile} does not have extra"


if __name__ == "__main__":
    test_rawid()
    test_rawurl()
    test_rawname()
    test_rawmeta()
    test_rawinfo()
    test_rawbasic()
    test_rawprofile()

#    test_dbdirargs()
    