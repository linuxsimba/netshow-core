""" Linux Kernel Spanning Tree module. Abstracts key STP info from the 802.1d
STP implementation in the Linux Kernel
"""

import netshowlib.linux.common as common


class Bridge(object):
    """ Spanning Tree Bridge attributes

    * **root_priority**: spanning tree root priority
    * **bridge_priority**: spanning tree priority of this bridge on this device
    * **root_id**: Bridge ID of root of STP
    * **bridge_id**: spanning tree bridge id
    * **mode**: stp mode. for this bridge type its only '802.1d'


    """
    def __init__(self, name):
        self._root_priority = None
        self._bridge_priority = None
        self._bridge_id = None
        self._root_id = None
        self.mode = '802.1d'

    @property
    def root_priority(self):
        """
        :return: bridge root priority
        """
        pass

    @property
    def bridge_id(self):
        """
        :return: return bridge ID
        """
        pass


class BridgeMember(object):
    """ Spanning Tree Bridge Member attributes

    * **bridge **: pointer to :class:`Bridge` instance the interface belongs to
    * **name**: name of the bridge member
    * **state**: can be 'forwarding', 'discarding', 'root'

    """
    def __init__(self, name, bridge):
        self.name = name
        self.bridge = bridge
        self._state = 0

    def _stp_state(self):
        """
        Possible options are

        * 0(*disabled*)
        * 1(*listening*)
        * 2(*learning*)
        * 3(*forwarding*)
        * 4(*blocking*)

        :return: stp state of the port
        """
        _attr = 'brport/state'
        return int(common.read_from_sys(_attr, self.name))

    def _is_root_port(self):
        """
        :return: true if port is root port of the switch
        """
        _attr = 'brport/designated_root'
        designated_root = common.read_from_sys(_attr, self.name)
        return True if designated_root == self.bridge.designated_root else False

    @property
    def state(self):
        """
        Possible options are

        * 0(*disabled*)
        * 1(*listening*)
        * 2(*learning*)
        * 3(*forwarding*)
        * 4(*blocking*)
        * 5(*root port*)

        :return_type: integer
        :return: port stp state using values shown above
        """
        if self._is_root_port():
            self._state = 5
        else:
            self._state = self._stp_state()

        return self._state
