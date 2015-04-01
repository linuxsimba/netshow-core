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
import netshowlib.cache as nc
from nose.tools import set_trace
import mock
from mock import MagicMock


@mock.patch('netshowlib.cache.nnlib.os_check')
@mock.patch('netshowlib.cache.nnlib.import_module')
def test_returning_cache(mock_import, mock_os_check):
    """ test return cache of a specific type """
    # mocks os check to return 'debian' and mocks the call
    # to 'netshowlib.debian.cache'.
    # when 'netshowlib.debian.cache.Cache' is called return
    # a string 'debian cache found'
    mock_os_check.return_value = 'debian'
    mock_debian_cache = MagicMock()
    mock_debian_cache.Cache.return_value = 'debian cache found'
    mock_import.return_value = mock_debian_cache
    assert_equals(nc.cache(), 'debian cache found')
