""" Linux Bridge Module tests
"""
# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
import netshowlib.linux.bridge as linux_bridge
import mock
from asserts import assert_equals
from nose.tools import set_trace


class TestLinuxBridge(object):
    """ Linux Bridge tests """

    def setup(self):
        """ setup function """
        self.iface = linux_bridge.Bridge('br0')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_vlan_filtering(self, mock_read_oneline):
        # vlan_filtering does not exist. Classic bridge.
        self.iface._vlan_filtering = False
        mock_read_oneline.return_value = None
        assert_equals(self.iface.vlan_filtering, False)
        mock_read_oneline.assert_called_with(
            '/sys/class/net/br0/bridge/vlan_filtering')
        # vlan_filtering exists and is set to 1 - New bridge driver enabled
        self.iface._vlan_filtering = False
        mock_read_oneline.return_value = '1'
        assert_equals(self.iface.vlan_filtering, True)
        # vlan_filtering exists and is set to 0
        self.iface._vlan_filtering = False
        mock_read_oneline.return_value = '0'
        assert_equals(self.iface.vlan_filtering, False)

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_get_list_of_bridge_members(self, mock_listdirs):
        bridgemems = ['swp8', 'swp9']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.members, bridgemems)
        mock_listdirs.assert_called_with('/sys/class/net/br0/brif')

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_get_tagged_bridge_members(self, mock_listdirs):
        bridgemems = ['swp7', 'swp8', 'swp9.100', 'swp10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.tagged_members, ['swp9.100', 'swp10.100'])

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_untagged_bridge_members(self, mock_listdirs):
        bridgemems = ['swp7', 'swp8', 'swp9.100', 'swp10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.untagged_members, ['swp7', 'swp8'])

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_vlan_tag(self, mock_listdirs):
        # single tag
        bridgemems = ['swp7', 'swp8', 'swp9.100', 'swp10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.vlan_tag, '100')
        # multiple tags
        bridgemems = ['swp7', 'swp8', 'swp9.100', 'swp10.100',
                      'swp11.10', 'swp12.3']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.vlan_tag, '3, 10, 100')
        #no tag
        bridgemems = ['swp7', 'swp8']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.vlan_tag, '')



