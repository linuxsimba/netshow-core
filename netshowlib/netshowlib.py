"""
This module does OS discovery , and Interface discovery

"""

import os
import glob
import operator
import re


def import_module(name):
    """
    from stack overflow.
    :param name: import path string like 'netshowlib.os_discovery.linux'
    :return: module matching the import statement

    """

    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
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

    # get dirname to this file. most likely absolute
    _dirname = os.path.dirname(__file__)
    # get a list of files under the os_discovery path
    _dir_entries = glob.glob("%s/os_discovery/[a-z]*.py" % _dirname)
    _os_types = {}
    # run os discovery check returns hash entries that look like this
    # { 'linux': 0 }. the integer is a priority . The lower the priority
    # the less likely the os is a match
    for _entry in _dir_entries:
        _entry_without_py = re.sub(r'\.py$', '', _entry)
        import_str = \
            "netshowlib.os_discovery.%s" % \
            os.path.basename(_entry_without_py)
        os_type = import_module(import_str)
        result = os_type.name_and_priority()
        if result:
            _os_types.update(result)

    if _os_types:
        return max(_os_types.items(), key=operator.itemgetter(1))[0].lower()
    # if no OS found, return none
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

    import_str = 'netshowlib.%s.iface' %  _ostype
    return import_module(import_str).iface_type(name, cache=cache)
