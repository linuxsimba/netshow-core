"""netshowlib module
This module is responsible for defining the `Iface` class at the root
of this library. When `netshowlib.Iface` is instantiated, it performs
a discovery through the library to return an `Iface` object that best
matches the characteristics of the interface.

For example: `netshowlib.Iface('eth1')` on a Debian Linux switch will
return an `Iface` object of type `netshowlib.debian.iface.Iface`
"""

class Iface(object):
    """Iface class
    This module instantiates an interface object that has methods and
    properties that best characterize the interface. For example calling
    `netshowlib.Iface('bond0') on a Ubuntu server will return an `Iface`
    object of type `netshowlib.linux.bond.Bond` because the class runs
    checks on the kernel to determine if the port is a bond and if true
    will return an object of type `Bond` in the correct OS class of `linux`
    """
    pass
