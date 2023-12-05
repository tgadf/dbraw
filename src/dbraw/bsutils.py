""" Useful utility functions for raw parsing """

__all__ = ["getTagText", "findTag", "isTag", "isBS4"]

import warnings
from bs4 import BeautifulSoup
from bs4.element import Tag


def isTag(tag: Tag) -> 'bool':
    return isinstance(tag, Tag)


def isBS4(bsdata: BeautifulSoup) -> 'bool':
    return isinstance(bsdata, BeautifulSoup)


def findTag(bsdata: Tag, name: str, params=None, default=None) -> 'Tag':
    if not isinstance(bsdata, (BeautifulSoup, Tag)):
        return None

    if isinstance(params, dict) and len(params) > 0:
        retval = bsdata.find(name, params)
    else:
        retval = bsdata.find(name)

    return retval
    

def getTagText(tag: Tag) -> 'str':
    if not isTag(tag):
        warnings.warn("tag is not a 'Tag' object")
        return ""

    retval = tag.text
    return retval