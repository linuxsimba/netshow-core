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
from asserts import assert_equals, mod_args_generator
from nose.tools import set_trace
from mock import MagicMock

class TestKernelStpBridgeMem(object):
    """ Kernel stp bridgemember class tests"""
    def setup(self):
        self.iface = linux_bridge.BridgeMember('eth1')
        self.stp = linux_bridge.KernelStpBridgeMember(self.iface)

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.iface.os.path.exists')
    @mock.patch('netshowlib.linux.common.read_symlink')
    def test_state_access_port(self, mock_symlink, mock_os_path,
                               mock_oneline):
        mock_subint = MagicMock()
        self.iface.get_sub_interfaces = mock_subint
        # bridgemember is access port
        mock_subint = []
        mock_symlink.return_value = 'br10'
        values = {
            '/sys/class/net/eth1/brport': True
        }
        values2 = {
            '/sys/class/net/eth1/brport/state': '3',
            '/sys/class/net/eth1/brport/designated_root': 'aaa',
            '/sys/class/net/eth1/brport/designated_bridge': 'aaa'
        }
        mock_oneline.side_effect = mod_args_generator(values2)
        mock_os_path.side_effect = mod_args_generator(values)
        briface = linux_bridge.Bridge('br10')
        linux_bridge.BRIDGE_CACHE['br10'] = briface
        assert_equals(self.stp.state, {
            'disabled': [],
            'blocking': [],
            'forwarding': [briface],
            'root': [briface],
            'intransition': [],
            'stp_disabled': []
        })

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    @mock.patch('netshowlib.linux.iface.os.path.exists')
    @mock.patch('netshowlib.linux.common.read_symlink')
    def test_state_trunk_port(self, mock_symlink, mock_os_path,
                              mock_oneline):
        mock_subint = MagicMock()
        mock_subint.return_value = ['eth1.11', 'eth1.20', 'eth1.30']
        self.iface.get_sub_interfaces = mock_subint
        # bridgemember is trunk port
        values = {
            '/sys/class/net/eth1/brport': True,
            '/sys/class/net/eth1.11/brport': True,
            '/sys/class/net/eth1.20/brport': False,
            '/sys/class/net/eth1.30/brport': True,
        }
        values2 = {
            '/sys/class/net/eth1/brport/state': '3',
            '/sys/class/net/eth1/brport/designated_root': 'aaa',
            '/sys/class/net/eth1/brport/designated_bridge': 'aaa',
            '/sys/class/net/eth1.11/brport/state': '0',
            '/sys/class/net/eth1.11/brport/bridge/bridge/stp_state': '1',
            '/sys/class/net/eth1.11/brport/designated_root': 'aaa',
            '/sys/class/net/eth1.11/brport/designated_bridge': 'aaa',
            '/sys/class/net/eth1.30/brport/state': '0',
            '/sys/class/net/eth1.30/brport/bridge/bridge/stp_state': '0'

        }
        values3 = {
            '/sys/class/net/eth1/brport/bridge': 'br10',
            '/sys/class/net/eth1.11/brport/bridge': 'br11',
            '/sys/class/net/eth1.20/brport/bridge': None,
            '/sys/class/net/eth1.30/brport/bridge': 'br30'
        }
        mock_symlink.side_effect = mod_args_generator(values3)
        mock_oneline.side_effect = mod_args_generator(values2)
        mock_os_path.side_effect = mod_args_generator(values)
        br10 = linux_bridge.Bridge('br10')
        br11 = linux_bridge.Bridge('br11')
        br30 = linux_bridge.Bridge('br30')
        linux_bridge.BRIDGE_CACHE['br10'] = br10
        linux_bridge.BRIDGE_CACHE['br11'] = br11
        linux_bridge.BRIDGE_CACHE['br30'] = br30
        assert_equals(self.stp.state, {
            'disabled': [br11],
            'blocking': [],
            'forwarding': [br10],
            'root': [br10, br11],
            'stp_disabled': [br30],
            'intransition': []
        })


class TestKernelStpBridge(object):
    def setup(self):
        br0 = linux_bridge.Bridge('br0')
        self.stp = linux_bridge.KernelStpBridge(br0)

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_get_root_priority(self, mock_read_oneline):
        mock_read_oneline.return_value = '8000.112233445566'
        assert_equals(self.stp.root_priority, '32768')
        mock_read_oneline.assert_called_with(
            '/sys/class/net/br0/bridge/root_id')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_get_bridge_priority(self, mock_read_oneline):
        mock_read_oneline.return_value = '4000.112233445566'
        assert_equals(self.stp.root_priority, '16384')
        mock_read_oneline.assert_called_with(
            '/sys/class/net/br0/bridge/root_id')


class TestLinuxBridgeMember(object):
    """ Linux Bridgemember tests"""

    def setup(self):
        """ setup function """
        self.iface = linux_bridge.BridgeMember('eth2')

    def test_attributes(self):
        assert_equals(isinstance(self.iface.stp,
                                 linux_bridge.KernelStpBridgeMember), True)


class TestLinuxBridge(object):
    """ Linux Bridge tests """

    def setup(self):
        """ setup function """
        self.iface = linux_bridge.Bridge('br0')

    @mock.patch('netshowlib.linux.common.read_file_oneline')
    def test_get_stp(self, mock_read_oneline):
        """ test getting STP """
        # if STP is disabled
        mock_read_oneline.return_value = '0'
        assert_equals(self.iface.stp, None)
        mock_read_oneline.assert_called_with('/sys/class/net/br0/bridge/stp_state')
        # if stp is enabled
        mock_read_oneline.return_value = '1'
        assert_equals(isinstance(self.iface.stp,
                                 linux_bridge.KernelStpBridge), True)

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
        assert_equals(sorted(list(self.iface.tagged_members.keys())),
                      sorted(['swp9', 'swp10']))

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
