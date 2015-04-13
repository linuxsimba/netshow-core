""" Linux ip neighbor module.
IP neighbor relationships in IPv4 are handled by Address Resolution Protocol
In IPv6 this process is just known as IP neighbor discovery.
"""

"""
'ipv4': ('00:00:11:11:22:22', '10.1.1.1'),
                      ('00:00:33:33:44:44', '10.1.1.3'),
             'ipv6': ('00:00:11:11:22:22', '10:1:1::1')
             }
            }
"""
def cacheinfo():
    """
    Example:

    .. code-block:: python
       >>   linux.arp.cacheinfo()
       >>> { 'eth1': linux.arp.Instance
             'eth2': linux.arp.Instance
           }

    :return arp ipv6 and ipv6 info via ip neighbor show
    """
    pass

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
        self._ipv4 = None
        self._ipv6 = None
        self._timer = None
        self._arp_filter = None
        self.name = name

    def run(self):
        pass

    @property
    def all_arps(self):
        pass

    @property
    def ipv4(self):
        pass

    @property
    def ipv6(self):
        pass

    @property
    def timer(self):
        pass

    @property
    def arp_filter(self):
        pass
