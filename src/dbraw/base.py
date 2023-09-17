""" Raw Base Data Class """

__all__ = ["RawBaseData", "MergeDict"]

#####################################################################################################################
# Main Raw Base Data Class
#####################################################################################################################
class RawBaseData:
    def __init__(self):
        self.err = None
        
    def get(self, key=None):
        retval = getattr(self,key) if (isinstance(key,str) and hasattr(self,key)) else self.__dict__
        return retval

    def mergeData(self, key, value):
        assert hasattr(self,key), f"RawData has no key [{key}]"
        selfValue = getattr(self, key)
        if isinstance(value,dict):
            if isinstance(selfValue,dict):
                setattr(self, key, MergeDict(selfValue, value).get())
            else:
                setattr(self, key, value)
        elif isinstance(value,list):
            if isinstance(selfValue,list):
                setattr(self, key, selfValue + value)
            else:
                setattr(self, key, value)
                
                
class MergeDict:
    def __init__(self, dctA, dctB):
        merged = dctA
        if all([isinstance(dct,dict) for dct in [dctA,dctB]]):
            for key,value in dctB.items():
                if value is None:
                    continue
                if isinstance(value,str) and len(value) == 0:
                    continue
                if merged.get(key) is None:
                    merged[key] = value
                else:
                    if all([isinstance(val,str) for val in [merged[key],value]]):
                        merged[key] = [merged[key],value]
                    elif all([isinstance(val,list) for val in [merged[key],value]]):
                        merged[key] += value
                    elif all([isinstance(val,dict) for val in [merged[key],value]]):
                        md = MergeDict(merged[key],value)                    
                        merged[key] = md.get()
                    
        self.merged = merged
        
    def get(self):
        return self.merged