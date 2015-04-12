""" Linux ARP module. """

def cacheinfo():
    pass

class Arp(object):
    """ Linux ARP Attributes
    See `Cumulus Networks Article on ARP <http://bit.ly/1NocSv1>`_ \
    for good explanation on the arp settings

    See `Cumulus Networks ARP Timer <http://bit.ly/1Nod8dl>`_ for \
    good explanation of ARP timer

    * **name**: name of interface
    * **cache**: pointer to :class:`netshowlib.linux.cache.Cache` instance
    * **ipv4**: ipv4 arp entries
    * **ipv6**: ipv6 arp entries
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
