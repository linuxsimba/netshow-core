""" Linux ip neighbor module.

IP neighbor relationships in IPv4 are handled by Address Resolution Protocol
In IPv6 this process is just known as IP neighbor discovery.

"""

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import netshowlib.linux.common as common


"""
'ipv4': ('00:00:11:11:22:22', '10.1.1.1'),
                      ('00:00:33:33:44:44', '10.1.1.3'),
             'ipv6': ('00:00:11:11:22:22', '10:1:1::1')
             }
            }
"""
def cacheinfo():
    """
    :return hash of of :class:`IpNeighbor` info by parsing ``ip neighbor show`` output.
    """
    # return empty ip neighbor dict
    ip_dict = {}
    _parse_ip_info(command='/sbin/ip -4 neighbor show',
                   iptype='ipv4',
                   ip_neigh_dict=ip_dict)
    _parse_ip_info(command='/sbin/ip -6 neighbor show',
                   iptype='ipv6',
                   ip_neigh_dict=ip_dict)

    return ip_dict

def _parse_ip_info(command, iptype, ip_neigh_dict):
    """
    parse ip neighbor information from either ipv4 or ipv6

    :params command: can be ``ip neigh show`` or ``ip -6 neigh show``
    :params iptype: can be ``ipv4`` or ``ipv6``
    :params ip_neigh_dict: dict to update neighbor table
    """
    try:
        neighbor_table = common.exec_command(command)
    except:
        return

    fileio = StringIO(neighbor_table)
    for line in fileio:
        if len(line.strip()) <= 0:
            continue
        ip_neigh_arr = line.split()
        if ip_neigh_arr[-1] == 'REACHABLE':
            _ip = ip_neigh_arr[0]
            ifacename = ip_neigh_arr[2]
            _mac = ip_neigh_arr[4]
            try:
                _instance = ip_neigh_dict[ifacename]
            except KeyError:
                _instance = IpNeighbor(ifacename)
                ip_neigh_dict[ifacename] = _instance

            _instance.__dict__[iptype][_ip] = {'mac': _mac}



class IpNeighbor(object):
    """ Linux IP neighbor attributes
    See `Cumulus Networks Article on ARP <http://bit.ly/1NocSv1>`_ \
    for good explanation on the arp settings

    See `Cumulus Networks ARP Timer <http://bit.ly/1Nod8dl>`_ for \
    good explanation of ARP timer

    * **name**: name of interface
    * **cache**: pointer to :class:`netshowlib.linux.cache.Cache` instance
    * **ipv4**: ipv4 neighbor entries
    * **ipv6**: ipv6 neighbor entries
    * **timer**: arp timer
    * **arp_filter**: ARP filter setting.
    * **arp_ignore**: ARP ignore setting.
    * **arp_notify**: ARP notify setting.
    * **arp_announce**: ARP announce setting.
    * **arp_accept**: ARP accept setting.
    """
    def __init__(self, name, cache=None):
        self._cache = cache
        self.ipv4 = {}
        self.ipv6 = {}
        self._timer = None
        self._arp_filter = None
        self.name = name

    def run(self):
        pass

    @property
    def all_neighbors(self):
        pass

    @property
    def timer(self):
        pass

    @property
    def arp_filter(self):
        pass
