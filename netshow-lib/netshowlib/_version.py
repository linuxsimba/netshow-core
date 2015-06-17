# pylint: disable=E1102
""" Assumes package is installed before checking
the version this way
"""
import pkg_resources


def get_version():
    """ get version """
    return pkg_resources.require('netshow-core-lib')[0].version
