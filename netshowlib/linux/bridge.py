""" This module is responsible for finding properties
related to linux bridge and bridge member interfaces """
import netshowlib.linux.iface as linux_iface
import os


def update_stp_state(stp_hash, iface_to_add, iface_under_test):
    """
    Updates stp state dict from BridgeMember and Bridge
    """
    iface_stp_state = iface_under_test.read_from_sys('brport/state')
    if iface_stp_state == '0':
        stp_hash.get('disabled').append(iface_to_add)
    elif iface_stp_state == '1' or iface_stp_state == '2':
        stp_hash.get('intransition').append(iface_to_add)
    elif iface_stp_state == '3':
        stp_hash.get('forwarding').append(iface_to_add)
    elif iface_stp_state == '4':
        stp_hash.get('blocking').append(iface_to_add)
    designated_root = iface_under_test.read_from_sys('brport/designated_root')
    designated_bridge = iface_under_test.read_from_sys('brport/designated_bridge')
    if designated_root == designated_bridge:
        stp_hash.get('root').append(iface_to_add)


class BridgeMember(linux_iface.Iface):
    """ Linux Bridge Member attributes

    * **state**:  stp vlan information for the port. Example:
    .. code-block:: python
       >> print(iface.state)
       >> { 'forwarding':  [list of bridges ],
            'blocking': [ list of bridges ],
            'root': [ list of bridges],
            'intransition': [ list of bridges]
          }
    """
    def __init__(self, name, cache=None):
        linux_iface.Iface.__init__(self, name, cache)
        self._state = {
            'disabled': [],
            'blocking': [],
            'forwarding': [],
            'root': [],
            'intransition': []
        }
        self._cache = cache

    def __str__(self):
        return "my name is %s" % self.name

    @property
    def state(self):
        """
        :return: dict of stp states with associated \
            :class:`linux.bridge<Bridge>` instances
        """
        self._state = {
            'disabled': [],
            'blocking': [],
            'forwarding': [],
            'root': [],
            'intransition': []
        }
        # go through list of subints look for bridge members
        # understand stp config for that interface and update
        # _state dict.
        for subintname in self.get_sub_interfaces():
            subiface = linux_iface.Iface(subintname)
            bridgename = subiface.read_symlink('brport/bridge')
            bridgeiface = Bridge(bridgename, cache=self._cache)
            if subiface.is_bridgemem():
                update_stp_state(self._state, bridgeiface, subiface)
        return self._state


class Bridge(linux_iface.Iface):
    """ Linux Bridge interface attributes

    * **tagged_members**: list of tagged bridge members *(part of a trunk)*
    * **untagged_members**: list of untagged bridge members *(access)*
    * **members**: all bridge members
    * **vlan_tag**: vlan ID tag if applicable. empty string means no tag.
    * **member_state**:  provides stp port state summary regarding the bridge members
    * **root_priority**: root priority for the spanning tree domain
    * **bridge_priority**: bridge priority


    """
    def __init__(self, name, cache=None):
        linux_iface.Iface.__init__(self, name, cache)
        self._tagged_members = {}
        self._untagged_members = {}
        self._members = {}
        self._vlan_tag = ''
        self._cache = cache
        self._member_state = {
            'disabled': [],
            'blocking': [],
            'forwarding': [],
            'root': [],
            'intransition': []
        }

    # -----------------

    def _memberlist_str(self):
        """
        :return: list of bridge member names. both tagged and untagged
        """
        dirlist = []
        try:
            dirlist = os.listdir(self.sys_path('brif'))
        except OSError:
            pass
        return dirlist

    def _get_members(self):
        """
        :return: get the members of a bridge into the tagged , untagged and total \
            member names and number structures
        """
        self._members = {}
        self._tagged_members = {}
        self._untagged_members = {}
        member_list = self._memberlist_str()
        for _name in member_list:
            # take the name of the main physical or logical interface
            # not the subinterface
            membername_arr = _name.split('.')
            bridgemem = BridgeMember(membername_arr[0],
                                     cache=self._cache)
            if len(membername_arr) == 2:
                self._tagged_members[membername_arr[0]] = bridgemem
            else:
                self._untagged_members[membername_arr[0]] = bridgemem
            self._members[membername_arr[0]] = bridgemem

    # ---------------------------

    @property
    def member_state(self):
        """
        :return: dict of stp state of bridge members
        """
        self._member_state = {
            'disabled': [],
            'blocking': [],
            'forwarding': [],
            'root': [],
            'intransition': []
        }

        # go through tagged members first
        for _ifacename, _iface in self.tagged_members.items():
            subifacename = "%s.%s" % (_ifacename, self.vlan_tag)
            subiface = linux_iface.Iface(subifacename)
            update_stp_state(self._member_state, _iface, subiface)

        for _ifacename, _iface in self.untagged_members.items():
            update_stp_state(self._member_state, _iface, _iface)

        return self._member_state

    @property
    def members(self):
        """
        :return: list of bridge port members
        """
        self._get_members()
        return self._members

    @property
    def tagged_members(self):
        """
        *Works for default/classic linux bridge driver*

        :return: list of tagged bridge members.
        """
        self._get_members()
        return self._tagged_members

    @property
    def untagged_members(self):
        """
        *Works for default/classic linux bridge driver*

        :return: list of untagged bridge members
        """
        self._get_members()
        return self._untagged_members

    @property
    def vlan_tag(self):
        """
        | For the vlan-aware bridge driver, a vlan tag is not applicable
        | For the classic/default bridge driver, if a tagged bridge member \
        is provided then the function will use the tag as the vlan id

        :return: vlan ID if applicable. If multiple tags found, possibly indicating \
            vlan translation, then all tags are printed as a comma \
            delimited string. Empty string means no tag.
        """

        # this may print something like '100,400', meaning that this bridge
        # is doing vlan translation. If string is empty('') then no tag is found
        # ----------------------
        # the messy looking function below is doing the following:
        # take a list of members ['eth1.100', 'eth2', 'eth3.100'], remove all untagged
        #   iface
        # take list of tagged members for example [ eth1.100', 'eth3.100']
        # strip off tag with list comprehension & put in array so it is ['100',100']
        # apply set() to the array so it removes all non-unique values. becomes
        # set([100])
        # then convert back to a list
        # then sorts it, uses the sorted([list] key=int)
        # apply str.join function on list.
        # on an empty tagged_member output it will produce ''
        # -----------------------------------
        self._vlan_tag = ', '.join(sorted(list(set(
            [x.split('.')[1] for x in self._memberlist_str()
             if len(x.split('.')) > 1])), key=int))
        return self._vlan_tag
