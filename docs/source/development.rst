Development
-----------

Library Structure
==================

netshow-lib has a core :mod:`~netshowlib` module that contains the
:class:`~netshowlib.Iface` object. The :class:`~netshowlib.Iface`
goes through OS Type specific modules to find the ``Iface`` object that
best matches the interface properties.

The netshow-lib directory structure looks like what is shown below

.. code-block:: shell

  ├── netshowlib
  │   ├── __init__.py
  │   ├── linux
  │   │   ├── common.py
  │   │   ├── bond.py
  │   │   ├── bridge.py
  │   │   ├── counters.py
  │   │   ├── lldp.py
  │   │   ├── lacp.py
  │   │   ├── iface.py
  │   │  
  │   ├── bsd
  │   │   ├── common.py
  │   │   ├── bond.py
  │   │   ├── bridge.py
  │   │   ├── counters.py
  │   │   ├── lldp.py
  │   │   ├── lacp.py
  │   │   ├── iface.py
  │   ├── lsb_release.py
  ├── netshowlib.py


Under each *OS Type* one defines a variety of **interface modules**, such as
*bridge*, *bond*

In addition to **interface modules** there are  **feature modules** such as
*stp*, *lacp*, *lldp*, *counters*.

Iface Structure
===============

For each OS Type, the ``iface.Iface`` class is the root. this class can inherit
the ``iface.Iface`` of another OS Type. For example one can create an OS type of
``debian`` and get ``debian.iface.Iface`` to be a child class of
``linux.iface.Iface``

These modules makes heavy use of
`Python propeties <https://docs.python.org/3/library/functions.html#property>`_. For example,
take the ``mtu`` property. If called, it will grab the latest value from the
kernel and cache it. If you wish to refresh it, clear the related variable that
starts with an *underscore*

.. code-block:: python

  eth0 = netshowlib.Iface('eth0')
  eth0.mtu
  >> 1500
  # will return current values.
  # subsequent calls to eth.mtu will not
  # produce the most recent value

  # to grab the latest value clear the _mtu value
  eth0._mtu = None
  eth0.mtu
  >> 9000

Some of the attributes are managed in other modules for example *stp*, or
*ipaddr*. These are called *features*.  How the values associated with these modules
are obtained and refreshed are discussed in the `next section
<development.html#feature-structure>`_



Port Bitmap Categorization
===========================

Port categorizations are captured in a port bitmap, which is described below

.. code-block:: python

  # linux/iface.py
  #---------------

  # Port is a bridge member
  L2_INT = 1

  # Port has an IP
  L3_INT = 2

  # Port has bridge members
  BRIDGE_INT = 3

  # Port has bond members
  BOND_INT = 4

  # Port is a bond member
  BONDMEM_INT = 5

  # Port is a switch port trunk
  TRUNK_INT = 6

  # Port is a management port
  MGMT_INT = 7

  # Port is a loopback
  LOOPBACK_INT = 8

  # Port is a front panel data port
  PHY_INT = 9

  # Port is a subinterface of a physical port or bond port
  SUB_INT = 10

  # Port is a subinterface of a bridge port.
  # Bridge port has Vlan filtering enabled
  SVI_INT = 11

  # Port is a VXLAN port.
  VXLAN_INT = 12


Here is an example of determining port type

.. code-block:: python

  import netshowlib

  bond0 = netshowlib.Iface('bond0')
  bond0.port_type
  >> 16
  bond0.is_bond()
  >> True
  bond0.is_bridge()
  >> False
  bond0.is_phy()
  >> False

Feature Structure
==================

These are modules that are not a type of interface, such as *lacp*, *stp*.
The basic structure of a feature module looks like this

.. code-block:: python

   # netshowlib/linux/my_feature.py


   def cacheinfo():
     """ get all possible values of this feature
     for example, get all LLDP values, or get all IP addresses
     not all features have caches, like the counters module
     """
     pass

   class MyFeature(object):
     """
     __init__ locates the specific feature attributes for the interface
     if cache is not specified then make the necessary calls to populate
     the feature object
     """
     def __init__(self, name, cache=None):
        """
        initialize attributes defined in this feature
        """
        self.name = _name
        self.cache = _cache

     def run(self, refresh=False):
       """
       populate the attributes defined in this feature from \
       either the cache data or directly from the system
       :param refresh: if true, and cache is enabled \
       will get the latest info from the system and not from the cache
       """


Here is an example of how to list lldp information from a cache

.. code-block:: python

  import netshowlib

  _cache = netshowlib.cache.cache()
  # gets lldp only cache
  _cache.run(feature=['lldp'])
  eth1 = netshowlib.Iface('eth1', _cache)
  eth1.lldp.adj_switch
  >> 'switch10'

The next example shows grabbing IP address info with no cache.
Every time you call ``ipaddr.ipv4`` it will make a call to the kernel files
and grab the info

.. code-block:: python

  eth0 = netshowlib.Iface('eth0')
  eth0.ipaddr.ipv4
  >>> ['192.168.0.12/24']


This example shows how to get the IP address using a cache.
A call to  ``ipaddr.ipv4`` will not trigger a call
to the kernel files and just use the cached info




.. code-block:: python

  _cache = netshowlib.cache.cache()
  _cache.run(feature=['ipaddr'])
  eth0 = netshowlib.Iface('eth0', _cache)
  eth.ipaddr.ipv4

To refresh the cache and check the IP address, call :meth:`Cache.run() <~netshowlib.linux.Cache.run>`
again and change the cache file

.. code-block:: python

  # refreshes cache
  _cache.run(feature=['ipaddr'])

  eth.ipaddr.ipv4


Also you can obtain the latest feature information directly from the system
without using a cache by setting the  ``refresh`` attribute to true

.. code-block:: python

  # will ignore the existing cache and create a new one specific
  # for ip address info and use that instead of what is found in
  # the netshowlib.cache.cache() instance
  eth.ipaddr.run(refresh=True)
  eth.ipaddr.ipv4
