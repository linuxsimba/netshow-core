""" Linux System Summary Info
"""
# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
from netshowlib.linux import system_summary
import mock
from asserts import assert_equals
from nose.tools import set_trace


class TestSystemSummary(object):

    @mock.patch('netshowlib.linux.system_summary.common.distro_info')
    def setup(self, mock_distro_info):
        mock_distro_info.return_value = {'RELEASE': '14.04',
                                         'ID': 'Ubuntu',
                                         'DESCRIPTION': 'Ubuntu 14.04.1 LTS'}
        self.systemsummary = system_summary.SystemSummary()

    def test_init(self):
        assert_equals(self.systemsummary.os_name, 'Ubuntu')
        assert_equals(self.systemsummary.os_build, 'Ubuntu 14.04.1 LTS')
        assert_equals(self.systemsummary.version, '14.04')

    @mock.patch('netshowlib.linux.system_summary.common.read_file_oneline')
    def test_uptime(self, mock_read_file):
        mock_read_file.return_value = '100'
        assert_equals(self.systemsummary.uptime, '100')
        mock_read_file.assert_called_with('/proc/uptime')
"""
from netshowlib.system_hw import SystemHw
import mock
from mock import MagicMock
from asserts import assert_equals
from nose.tools import set_trace


class TestSystemHw():

    @mock.patch('netshowlib.system_hw.distro_info')
    def setup(self, mock_distro_info):
        mock_distro_info.return_value = {'RELEASE': '14.04',
                                         'ID': 'Ubuntu',
                                         'DESCRIPTION': 'Ubuntu 14.04.1 LTS'}
        self.syshw = SystemHw()

    @mock.patch('netshowlib.system_hw.read_file_oneline')
    def test_get_uptime(self, mock_read_file):
        mock_read_file.return_value = '100'
        self.syshw.get_uptime()
        assert_equals(self.syshw.uptime, '100')
        mock_read_file.assert_called_with('/proc/uptime')

    @mock.patch('netshowlib.system_hw.SystemHw.get_uptime')
    @mock.patch('netshowlib.system_hw.platform.machine')
    def test_get_system_version(self, mock_platform,
                                mock_uptime):
        mock_platform.return_value = 'ppc'
        self.syshw.uptime = '10000'
        self.syshw.get_system_version()
        assert_equals(self.syshw.version, '14.04')
        assert_equals(self.syshw.os_name, 'Ubuntu')
        assert_equals(self.syshw.build, 'Ubuntu 14.04.1 LTS')

    # get generic platform info.
    # for not its blank
    def test_get_platform_info(self):
        assert_equals(self.syshw.get_platform_info(), None)

"""
