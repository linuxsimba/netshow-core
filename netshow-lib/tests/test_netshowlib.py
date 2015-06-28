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
import mock
import sys
from mock import MagicMock


def test_import_module():
    """ test import module """
    ospath = nn.import_module('os.path')
    assert_equals(ospath.exists('/etc/hosts'), True)


@mock.patch('netshowlib.netshowlib.os.path.dirname')
@mock.patch('netshowlib.netshowlib.glob.glob')
@mock.patch('netshowlib.netshowlib.import_module')
def test_provider_check(mock_import,
                        mock_glob,
                        mock_os_dirname):
    """ test os discovery """
    # return a directory with 3 OS types, each will return different priorities
    # choose the one with the highest priority
    mock_glob.return_value = ['path/providers/linux',
                              'path/providers/debian',
                              'path/providers/ubuntu']
    mock_linux = MagicMock()
    mock_linux.name_and_priority.return_value = {'Linux': 0}
    mock_debian = MagicMock()
    mock_debian.name_and_priority.return_value = {'Debian': 1}
    mock_debian = MagicMock()
    mock_debian.name_and_priority.return_value = {'Ubuntu': 2}
    mock_os_dirname.return_value = 'netshowlib'
    values = {
        'netshowlib.linux.provider_discovery': mock_linux,
        'netshowlib.debian.provider_discovery': mock_debian,
        'netshowlib.ubuntu.provider_discovery': mock_debian
    }
    mock_import.side_effect = mod_args_generator(values)
    assert_equals(nn.provider_check(), 'ubuntu')

    sys.real_prefix = 'blah'
    nn.provider_check()
    mock_glob.assert_called_with(sys.prefix + '/share/netshow-lib/providers/*')


@mock.patch('netshowlib.netshowlib.provider_check')
@mock.patch('netshowlib.netshowlib.import_module')
def test_iface_discovery(mock_import, mock_provider_check):
    """ test iface discovery """
    # provider_check is none
    mock_provider_check.return_value = 'debian'
    mock_debian_iface = MagicMock()
    mock_debian_iface.iface.return_value = 'its a debian bridge'
    values = {'netshowlib.debian.iface': mock_debian_iface}
    mock_import.side_effect = mod_args_generator(values)
    assert_equals(nn.iface('eth1'), 'its a debian bridge')
    # if provider_check is not none
    mock_debian_iface = MagicMock()
    mock_debian_iface.iface.return_value = 'its a debian bridge'
    values['netshowlib.debian.iface'] = mock_debian_iface
    assert_equals(nn.iface('eth1', providername='debian'), 'its a debian bridge')
    # if cache is set provider_check is none
    mock_debian_iface.reset_mock()
    mock_debian_iface = MagicMock()
    mock_debian_iface.iface.return_value = 'its a debian bridge'
    mock_debian_cache = MagicMock()
    values = {'netshowlib.debian.iface': mock_debian_iface,
              'netshowlib.debian.cache': mock_debian_cache}
    mock_import.side_effect = mod_args_generator(values)
    all_cache = nn.feature_cache()
    assert_equals(nn.iface('eth1', cache=all_cache),
                  'its a debian bridge')
    # confirm syntax for iface_type accepts cache
    mock_debian_iface.iface.assert_called_with('eth1', cache=all_cache)


@mock.patch('netshowlib.netshowlib.provider_check')
@mock.patch('netshowlib.netshowlib.import_module')
def test_portlist(mock_import, mock_provider_check):
    mock_provider_check.return_value = 'debian'
    mock_debian_iface = MagicMock()
    mock_debian_iface.portname_list.return_value = ['eth22', 'eth33']
    values = {
        'netshowlib.debian.iface': mock_debian_iface
    }
    mock_import.side_effect = mod_args_generator(values)
    assert_equals(nn.portname_list(), ['eth22', 'eth33'])
