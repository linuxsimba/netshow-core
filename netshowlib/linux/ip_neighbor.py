""" Linux ip neighbor module.

IP neighbor relationships in IPv4 are handled by Address Resolution Protocol
In IPv6 this process is just known as IP neighbor discovery.

"""

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import netshowlib.linux.common as common


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

    decoded_str = neighbor_table.decode('utf-8')
    fileio = StringIO(decoded_str)
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
                _instance = {'ipv4': {},
                             'ipv6': {}}
                ip_neigh_dict[ifacename] = _instance

            _instance[iptype][_ip] = {'mac': _mac}


class IpNeighbor(object):
    """ Linux IP neighbor attributes

    * **name**: name of interface
    * **cache**: pointer to :class:`netshowlib.linux.cache.Cache` instance
    * **ipv4**: ipv4 neighbor entries
    * **ipv6**: ipv6 neighbor entries
    """
    def __init__(self, name, cache=None):
        self._cache = cache
        self.ipv4 = {}
        self.ipv6 = {}
        self.name = name

    def run(self):
        """
        collect IP neighbor entries and grab the one associated with this interface
        """
        if self._cache:
            return



    @property
    def all_neighbors(self):
        self.run()
        return self.ipv4 + self.ipv6
