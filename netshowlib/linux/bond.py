""" This module is responsible for finding properties
related to bond interface and bond member interfaces """
import netshowlib.linux.iface as linux_iface
import netshowlib.linux.lacp as lacp
import re
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class Bond(linux_iface.Iface):
    """ Linux Bond attributes

    * **members**: list of bond members/slaves. creates instances of \
    :class:`BondMember<netshowlib.linux.bond_member.BondMember>`
    * **bond mode**: options are

      * *balance-rr    '0'*
      * *active-backup '1'*
      * *balance-xor   '2'*
      * *balance-alb   '3'*
      * *802.3ad       '4'*
      * *balance-tlb   '5'*
      * *balance-alb   '6'*

    * **min_links**: number of minimum links
    * **hash_policy**: load balancing algorithm. options are

      * *layer2    '0'*
      * *layer3+4  '1'*

    * **lacp**: pointer to :class:`Lacp instance<netshowlib.linux.lacp.Lacp>` for this \
        bond
    * **system_mac**: Bond system mac. Packets egressing bond use this mac address.

    """
    def __init__(self, name, cache=None):
        linux_iface.Iface.__init__(self, name, cache)
        self._members = {}
        self._mode = None
        self._min_links = None
        self._hash_policy = None
        self._lacp = None
        self._system_mac = None

    # -------------------

    def parse_proc_net_bonding(self, bondfile):
        """
        parse ``/proc/net/bonding`` of this bond to get the system mac
        eventually this info will be in the kernel. I believe its
        kernel 3.18 or something. will confirm with a kernel dev.

        :param bondfile: path to /proc/net file for the bond
        """
        try:
            result = open(bondfile).read()
        except IOError:
            return
        fileio = StringIO(result)
        for line in fileio:
            if len(line.strip()) <= 0:
                continue
            # make all char lowercase
            line = line.lower()
            # determine mac address of the bond
            if re.match(r'system\s+identification', line):
                self._system_mac = line.split()[-1]
                continue

    # ---------------------
    # Define properties

    @property
    def members(self):
        """
        :return: list of bond members
        """
        fileoutput = self.read_from_sys('bonding/slaves')
        # if bond member list has changed..clear the bond members hash
        if fileoutput:
            if set(fileoutput.split()) != set(self._members.keys()):
                self._members = {}
                for i in fileoutput.split():
                    self._members[i] = BondMember(i, self)
        else:
            self._members = {}

        return self._members

    @property
    def mode(self):
        """
        :return: bond mode integer. Not the name. See \
            `linux kernel driver docs <http://bit.ly/1BSyeVh>`_ for more details
        """
        self._mode = None
        fileoutput = self.read_from_sys('bonding/mode')
        if fileoutput:
            self._mode = fileoutput.split()[1]
        return self._mode

    @property
    def min_links(self):
        """
        :return: number of minimum links required to keep the bond active
        """
        self._min_links = self.read_from_sys('bonding/min_links')
        return self._min_links

    @property
    def hash_policy(self):
        """
        :return: bond load balancing policy / xmit hash policy
        """
        self._hash_policy = None
        fileoutput = self.read_from_sys('bonding/xmit_hash_policy')
        if fileoutput:
            self._hash_policy = fileoutput.split()[1]
        return self._hash_policy

    @property
    def lacp(self):
        """
        :return: :class:`linux.lacp<netshowlib.linux.lacp.Lacp>` class instance if \
            bond is in LACP mode

        """
        if self.mode == '4':
            if not self._lacp:
                self._lacp = lacp.Lacp(self.name)
            return self._lacp
        return None


    @property
    def system_mac(self):
        """
        :return: bond system mac
        """
        self._system_mac = None
        bond_proc_file = "/proc/net/bonding/%s" % (self.name)
        self.parse_proc_net_bonding(bond_proc_file)
        return self._system_mac


class BondMember(linux_iface.Iface):
    """ Linux Bond Member Attributes

    * **master**: pointer to :class:`Bond<netshowlib.linux.bond.Bond>` instance \
        that this interface belongs to.
    * **link_failures**: bond driver reports number of times bond member flaps
    * **state**: returns whether bond member is active (1) or inactive(0) in a bond \
        **irrespective** of its carrier/linkstate status. What this means is that \
        the link can be up, but not in the bond.
    Examples:

    .. code-block:: python

        import netshowlib.netshowlib as nn

        # bond member info should be normally obtained from
        # first calling the bond and then running the members
        # property.
        bond0 = nn.bond.Bond('bond0')
        bond0.members
        >>[ output ]

        # on the rare case you know the bond member but want to get
        # bond master information you can.
        bondmem = nn.bond_member.BondMember('eth1')
        bondmem.master
        >> [ output ]

    """
    def __init__(self, name, cache=None, master=None):
        linux_iface.Iface.__init__(self, name, cache)
        self._master = master
        self._link_failures = None
        self._state = None

    # -------------------

    # Define properties

    @property
    def master(self, bondmaster=None):
        """
        :return: pointer to  :class:`Bond<netshowlib.linux.bond.Bond>` instance that \
        this interface belongs to
        """
        if not self._master:
            if bondmaster:
                self._master = bondmaster
            else:
                bondname = self.read_symlink('master')
                self._master = Bond(bondname)
        return self._master
