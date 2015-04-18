"""
This module does OS discovery , and Interface discovery

"""

import os
import glob
import operator
import sys


def import_module(mod_str):
    """
    inspired by post on stackoverflow
    :param name: import path string like 'netshowlib.os_discovery.linux'
    :return: module matching the import statement

    """

    _module = __import__(mod_str)
    _mod_parts = _module.split('.')
    for _mod_part in _mod_parts[1:]:
        mod = getattr(mod, mod_part)
    return mod


def os_check():
    """
    | **OS discovery check**
    looks into ``netshowlib/os_discovery`` path for any OS discovery files, and runs \
    the ``name_and_priority()`` function. If this function returns a hash with an \
    operating system name and priority, then this is put in a dict. \
    The OS with the max priority is chosen as the desired OS to use and the OS name \
    is returned

    :return: OS name of best match.
    """

    # get a list of files under the os_discovery path
    root_prefix = ''
    if hasattr(sys, 'real_prefix'):
        root_prefix = sys.prefix

    _dir_entries = glob.glob(root_prefix + "/var/lib/netshow-lib/discovery/*")
    _os_types = {}
    # run os discovery check returns hash entries that look like this
    # { 'linux': 0 }. the integer is a priority . The lower the priority
    # the less likely the os is a match
    for _entry in _dir_entries:
        import_str = \
            "netshowlib.%s.os_discovery" % \
            os.path.basename(_entry)
        os_type = import_module(import_str)
        result = os_type.name_and_priority()
        if result:
            _os_types.update(result)

    if _os_types:
        return max(_os_types.items(), key=operator.itemgetter(1))[0].lower()
    # if no OS found, return none
    return None


def feature_cache():
    """
    Performs OS discovery and returns the OS appropriate Cache() module
    """
    os_type = os_check()
    if os_type:
        cache_path = "netshowlib.%s.cache" % os_type
        cache_module = import_module(cache_path)
        return cache_module.Cache()
    return None


def iface(name, os_type=None, cache=None):
    """
    | **Interface Discovery **
    looks into ``netshowlib/[os_type]/iface/iface_type`` to get the correct
    interface type

    :return:  Iface object that best matches interface characteristics
    """
    _ostype = os_type
    if not _ostype:
        _ostype = os_check()

    import_str = 'netshowlib.%s.iface' % _ostype
    return import_module(import_str).iface_type(name, cache=cache)
