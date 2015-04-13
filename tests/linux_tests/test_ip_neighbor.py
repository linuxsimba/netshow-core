# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
# pylint: disable=E0611
from asserts import assert_equals, mod_args_generator
from nose.tools import set_trace
import mock
from netshowlib.linux import ip_neighbor


@mock.patch('netshowlib.linux.ip_neighbor.common.exec_command')
def test_cacheinfo(mock_arp_exec):
    values = {
        '/sbin/ip -4 neighbor show':
        open('tests/linux_tests/arp_ipv4.txt').read(),
        '/sbin/ip -6 neighbor show':
        open('tests/linux_tests/arp_ipv6.txt').read()
    }

    mock_arp_exec.side_effect = mod_args_generator(values)
    result = ip_neighbor.cacheinfo()
    assert_equals(len(result.get('eth0').ipv4), 1)
    assert_equals(len(result.get('eth0').ipv6), 0)
    assert_equals(len(result.get('vlan1').ipv4), 7)
    assert_equals(len(result.get('vlan1').ipv6), 4)


"""
# parse single arp entry.
def test_parse_arp_entry():
    arp_dict = {}
    _line = '10:100:1::1 dev vlan1 lladdr 00:02:00:00:00:0a router REACHABLE'
    parse_arp_entry(_line, arp_dict)
    assert_equals(arp_dict['vlan1'].arp,
                  {'10:100:1::1': '00:02:00:00:00:0a'})


# correctly parse arp table if only has single table
@mock.patch('netshowlib.arp.exec_command')
def test_parse_arp_table(mock_arp_exec):
    mock_arp_exec.return_value = \
        '10:100:1::1 dev vlan1 lladdr 00:02:00:00:00:0a router REACHABLE'
    result = parse_arp_table()
    assert_equals(list(result.keys()), ['vlan1'])
    assert_equals(result['vlan1'].arp, {'10:100:1::1': '00:02:00:00:00:0a'})

"""
