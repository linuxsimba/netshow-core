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


    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_get_list_of_bridge_members(self, mock_listdirs):
        bridgemems = ['swp8', 'swp9']
        mock_listdirs.return_value = bridgemems
        assert_equals(sorted(list(self.iface.members.keys())), sorted(bridgemems))
        assert_equals(isinstance(self.iface.members.get('swp8'),
                                 linux_bridge.BridgeMember), True)
        mock_listdirs.assert_called_with('/sys/class/net/br0/brif')

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_get_tagged_bridge_members(self, mock_listdirs):
        bridgemems = ['swp7', 'swp8', 'swp9.100', 'swp10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(sorted(list(self.iface.tagged_members.keys())), sorted(['swp9', 'swp10']))

    @mock.patch('netshowlib.linux.bridge.os.listdir')
    def test_untagged_bridge_members(self, mock_listdirs):
        bridgemems = ['swp7', 'swp8', 'swp9.100', 'swp10.100']
        mock_listdirs.return_value = bridgemems
        assert_equals(sorted(list(self.iface.untagged_members.keys())),
                      sorted(['swp7', 'swp8']))

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
        # no tag
        bridgemems = ['swp7', 'swp8']
        mock_listdirs.return_value = bridgemems
        assert_equals(self.iface.vlan_tag, '')
