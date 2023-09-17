from dbraw import RawDataFileIO
from utils import FileIO, DirInfo
from os import getcwd


def test_datafileio():
    fID = "12345"
    fData = {"ID": fID, "URL": "http://www.something.com", "Name": "My Name"}
    rawdata = {fID: fData}
    dinfo = DirInfo(getcwd())
    finfo = dinfo.join("dummydata.p")
    io = FileIO()
    io.save(idata=rawdata, ifile=finfo)

    rawdfio = RawDataFileIO(fID=fID, fData=fData, ifile=finfo)
    
    fid = rawdfio.getID()
    assert fid == "12345", f"fid [{fid}] is not correct!"

    ifile = rawdfio.getFile()
    assert ifile == finfo, f"ifile [ifile] does not equal input [{finfo}]"
    
    bsdata = rawdfio.getData()
    assert bsdata == fData, f"bsdata [{bsdata}] does not equal input [{fData}]"
    
    finfo.rmFile()

    
if __name__ == "__main__":
    test_datafileio()
