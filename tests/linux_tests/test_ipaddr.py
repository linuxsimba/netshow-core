# disable docstring checking
# pylint: disable=C0111
# disable checking no-self-use
# pylint: disable=R0201
# pylint: disable=W0212
# pylint: disable=W0201
# pylint: disable=F0401
# pylint: disable=W0613
import netshowlib.linux.ipaddr as ipaddr_mod
import netshowlib.linux.cache as feature_cache
from asserts import assert_equals
from nose.tools import set_trace
import mock

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TestLinuxIpaddr(object):

    def test_ips(self):
        self.ipaddr = ipaddr_mod.Ipaddr('eth1')
        self.ipaddr.ipv4 = ['10.1.1.1/24']
        self.ipaddr.ipv6 = ['10:1:1::1/64']
        assert_equals(self.ipaddr.allentries, ['10.1.1.1/24', '10:1:1::1/64'])

    @mock.patch('netshowlib.linux.ipaddr.parse_ip_cache')
    def test_cacheinfo(self, mock_parse):
        mock_parse.return_value = "hash of ips"
        result = ipaddr_mod.cacheinfo()
        assert_equals(result, "hash of ips")

    @mock.patch('netshowlib.linux.ipaddr.cacheinfo')
    def test_run_ipaddr(self, mock_ip_cache):
        """ get ipv6 and ipv4 info """
        # using feature cache
        _output = open('tests/linux_tests/ip_addr_show.txt').read()
        output = StringIO(_output)
        mock_ip_cache.return_value = ipaddr_mod.parse_ip_cache(output)
        _feature_cache = feature_cache.Cache()
        ipaddr = ipaddr_mod.Ipaddr('eth0', _feature_cache)
        ipaddr.run()
        assert_equals(ipaddr.ipv4, ['192.168.0.33/24'])
        assert_equals(ipaddr.ipv6, [])
        # without feature cache
        ipaddr = ipaddr_mod.Ipaddr('eth0')
        ipaddr.run()
        assert_equals(ipaddr.ipv4, ['192.168.0.33/24'])
        assert_equals(ipaddr.ipv6, [])

    def test_parse_ip_cache(self):
        """ testing parsing ip cache info """
        _output = open('tests/linux_tests/ip_addr_show.txt').read()
        output = StringIO(_output)
        result = ipaddr_mod.parse_ip_cache(output)
        assert_equals(
            result,
            {
                'lo': {
                    'ipv4': [],
                    'ipv6': []
                },
                'net2compute': {
                    'ipv4': ['192.168.50.1/24'],
                    'ipv6': []
                },
                'virbr0': {
                    'ipv4': ['192.168.122.1/24'],
                    'ipv6': []
                },
                'vnet0': {
                    'ipv4': [],
                    'ipv6': []
                },
                'eth0': {
                    'ipv4': ['192.168.0.33/24'],
                    'ipv6': []
                }
            })
