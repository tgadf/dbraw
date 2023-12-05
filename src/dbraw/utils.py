""" Useful utility functions for raw parsing """

__all__ = ["getYear", "getTimestamp", "getJSON"]

import warnings
from pandas import Timestamp, to_datetime, NaT
import json


def getYear(value: str) -> 'int':
    if not isinstance(value, str):
        # warnings.warn(f"Could not get year from non-str input: {value}")
        return None

    tstamp = getTimestamp(value)
    if tstamp is NaT:
        year = None
    elif tstamp is None:
        year = None
    elif isinstance(tstamp, Timestamp):
        year = tstamp.year
    else:
        raise TypeError(f"to_datetime returned something unknown: {type(tstamp)}")
    
    return year
    

def getTimestamp(value: str) -> 'Timestamp':
    if not isinstance(value, str):
        # warnings.warn(f"Could not get year from non-str input: {value}")
        return None

    try:
        tstamp = to_datetime(value, errors='coerce')
    except Exception as error:
        tstamp = None
        warnings.warn(f"Could coerce year from {value}: {error}")

    return tstamp


def getJSON(value: str) -> 'dict':
    if not isinstance(value, str):
        warnings.warn(f"Could not load json from non-str input: {value}")
        return {}
    
    try:
        jData = json.loads(value)
    except Exception as error:
        warnings.warn(f"Could determine load json: {error}")
        jData = {}

    return jData