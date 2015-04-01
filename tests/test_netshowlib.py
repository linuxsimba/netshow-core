# http://pylint-messages.wikidot.com/all-codes
# pylint: disable=R0913
# disable unused argument
# pylint: disable=W0613
# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# disable invalid name
# pylint: disable=C0103
# pylint: disable=F0401
# pylint: disable=E0611
# pylint: disable=W0611
from asserts import assert_equals, mod_args_generator
import netshowlib.netshowlib as nn
import netshowlib.cache
from nose.tools import set_trace
import mock
from mock import MagicMock
import os


def test_import_module():
    """ test import module """
    ospath = nn.import_module('os.path')
    assert_equals(ospath.exists('/etc/hosts'), True)


@mock.patch('netshowlib.netshowlib.os.path.dirname')
@mock.patch('netshowlib.netshowlib.glob.glob')
@mock.patch('netshowlib.netshowlib.import_module')
def test_os_check(mock_import,
                  mock_glob,
                  mock_os_dirname):
    """ test os discovery """
    # test that dirname used is correct
    _loc = __file__ + '../../../netshowlib/netshowlib.py'
    _abspath = os.path.abspath(_loc)
    # delete compiled pyc file
    if os.path.exists(_abspath + 'c'):
        os.unlink(_abspath + 'c')
    nn.os_check()
    mock_os_dirname.assert_called_with(_abspath)

    # return a directory with 3 OS types, each will return different priorities
    # choose the one with the highest priority
    mock_glob.return_value = ['something/linux.py',
                              'something/debian.py',
                              'something/debian.py']
    mock_linux = MagicMock()
    mock_linux.name_and_priority.return_value = {'Linux': 0}
    mock_debian = MagicMock()
    mock_debian.name_and_priority.return_value = {'Debian': 1}
    mock_debian = MagicMock()
    mock_debian.name_and_priority.return_value = {'Ubuntu': 2}
    mock_os_dirname.return_value = 'netshowlib'
    values = {
        'netshowlib.os_discovery.linux': mock_linux,
        'netshowlib.os_discovery.debian': mock_debian,
        'netshowlib.os_discovery.debian': mock_debian
    }
    mock_import.side_effect = mod_args_generator(values)
    assert_equals(nn.os_check(), 'ubuntu')


@mock.patch('netshowlib.netshowlib.os_check')
@mock.patch('netshowlib.netshowlib.import_module')
def test_iface_discovery(mock_import, mock_os_check):
    """ test iface discovery """
    # os_check is none
    mock_os_check.return_value = 'debian'
    mock_debian_iface = MagicMock()
    mock_debian_iface.iface_type.return_value = 'its a debian bridge'
    values = {'netshowlib.debian.iface': mock_debian_iface}
    mock_import.side_effect = mod_args_generator(values)
    assert_equals(nn.iface('eth1'), 'its a debian bridge')
    # if os_check is not none
    mock_debian_iface = MagicMock()
    mock_debian_iface.iface_type.return_value = 'its a debian bridge'
    values['netshowlib.debian.iface'] = mock_debian_iface
    assert_equals(nn.iface('eth1', os_type='debian'), 'its a debian bridge')
    # if cache is set os_check is none
    mock_debian_iface.reset_mock()
    mock_debian_iface = MagicMock()
    mock_debian_iface.iface_type.return_value = 'its a debian bridge'
    mock_debian_cache = MagicMock()
    values = {'netshowlib.debian.iface': mock_debian_iface,
              'netshowlib.debian.cache': mock_debian_cache}
    mock_import.side_effect = mod_args_generator(values)
    all_cache = netshowlib.cache.cache()
    assert_equals(nn.iface('eth1', cache=all_cache),
                  'its a debian bridge')
    # confirm syntax for iface_type accepts cache
    mock_debian_iface.iface_type.assert_called_with('eth1', cache=all_cache)
