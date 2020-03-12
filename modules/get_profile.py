"""
source information from .gel_config file
"""
import json
import os

def get_profile(f=os.path.expanduser(".gel_config"), items=None):
    """
    get GEL profile details from file
    see https://cnfl.extge.co.uk/pages/viewpage.action?pageId=113196964 for
    details
    :param f: location of config file, default is ~/.gel_config
    :param items: string or list of items in gel_config to return
    """
    # get file contents
    with open(f) as json_file:
        d = json.load(json_file)

    # filter out the items from the object (including .defaults)
    if items is not None:
        if type(items) is str:
            items = [items]
        d = {k: v for k, v in d.items() if k in items or k == '.defaults'}

    # do the default replacement
    replace_defaults(d)
    return d


def recursive_search_replace(x, s, r):
    """
    recursively search and replace within dictionary
    :param x: dictionary item to replace in
    :param s: string to find
    :param r: string to replace s with
    """
    for k, v in x.items():
        if type(v) is dict:
            recursive_search_replace(v, s, r)
        else:
            if v == s:
                x[k] = r


def replace_defaults(d):
    """
    search and replace defaults in config dictionary
    removes defaults section in the process
    :param d: dictionary item
    """
    # remove the defaults section
    defaults = d.pop('.defaults')
    # do search and replace for each item in it
    for k, v in defaults.items():
        recursive_search_replace(d, '!' + k + '!', v)

