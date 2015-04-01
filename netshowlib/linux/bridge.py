""" This module is responsible for finding properties
related to linux bridge interfaces """
import netshowlib.linux.iface as linux_iface
import os
import re

class Bridge(linux_iface.Iface):
    """ Linux Bridge interface attributes

    * **tagged_members**: list of tagged bridge members *(part of a trunk)*
    * **untagged_members**: list of untagged bridge members *(access)*
    * **members**: all bridge members
    * **vlan_filtering**: if true \
    `vlan filtering <http://lwn.net/Articles/538877/>`_ is enabled
    * **vlan_tag**: vlan ID tag if applicable. empty string means no tag.


    """
    def __init__(self, name, cache=None):
        linux_iface.Iface.__init__(self, name, cache)
        self._tagged_members = []
        self._untagged_members = []
        self._members = []
        self._vlan_filtering = False
        self._vlan_tag = ''

    @property
    def vlan_filtering(self):
        """
        :return: true if  ``/sys/class/net/[iface]/vlan_filtering`` exists
        """
        vlan_filtering = self.read_from_sys('bridge/vlan_filtering')
        if vlan_filtering and int(vlan_filtering) == 1:
            self._vlan_filtering = True
        return self._vlan_filtering

    @property
    def members(self):
        """
        :return: list of bridge port members
        """
        try:
            self._members = os.listdir(self.sys_path('brif'))
        except OSError:
            pass
        return self._members


    @property
    def tagged_members(self):
        """
        *Works for default/classic linux bridge driver*

        :return: list of tagged bridge members.
        """
        self._tagged_members = []
        for i in self.members:
            _match = re.match(self.subint_port_regex(), i)
            if _match:
                self._tagged_members.append(_match.group(0))
        return self._tagged_members

    @property
    def untagged_members(self):
        """
        *Works for default/classic linux bridge driver*

        :return: list of untagged bridge members
        """
        self._untagged_members = []
        for i in self.members:
            _match = re.match(self.subint_port_regex(), i)
            if not _match:
                self._untagged_members.append(i)
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
        # Do nothing if bridge is vlan-aware
        if self.vlan_filtering:
            return

        # this may print something like '100,400', meaning that this bridge
        # is doing vlan translation. If string is empty('') then no tag is found
        # ----------------------
        # the messy looking function below is doing the following:
        # take list of tagged members for example ['swp1.100', 'swp2.100']
        # strip off tag with map func & put in array so it is ['100',100']
        # apply set() to the array so it removes all non-unique values. becomes
        # set([100])
        # then convert back to a list
        # then sorts it, uses the sorted([list] key=int)
        # apply str.join function on list.
        # on an empty tagged_member output it will produce ''
        #-----------------------------------
        self._vlan_tag = ', '.join(sorted(list(set(
            [x.split('.')[1] for x in self.tagged_members])), key=int))
        return self._vlan_tag

