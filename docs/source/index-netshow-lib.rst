**************************************
The Netshow Library (netshow-lib)
**************************************
.. toctree::
    :maxdepth: 2

    features-netshowlib.rst
    installation.rst
    development-netshowlib.rst
    provider_discovery.rst
    iface_discovery.rst
    api-netshow-lib.rst
    license.rst
    credits.rst


Introduction
------------

netshow-lib is a Python library that describes interface objects and associated network information relevant
to that interface. Originally developed to work with Cumulus Linux, it can work on any Linux system.
The library is useful in Linux systems with lots of interfaces like hypervisors and switches

Below is a simple example.
Get LLDP information for an interface. Using ``iface()`` activates provider discovery.

::

  from netshowlib import netshowlib as nn

  # Create iface object
  eth0 = netshowlib.iface('eth0')

  print (netshowlib.provider_check())
  >> 'linux'

  # print lldp information from linux system
  print(iface.lldp)
  >>  [{'adj_port': 'fe:42:9d:ff:bb:d0', 'adj_mgmt_ip': '192.168.0.13', 'adj_hostname': 'other-server'}]


Using a specific provider, which doing provider discovery

::

  from netshowlib import netshowlib as nn

  iface = nn.linux.Iface('eth0')

  print(iface.lldp)
  >>  [{'adj_port': 'fe:42:9d:ff:bb:d0', 'adj_mgmt_ip': '192.168.0.13', 'adj_hostname': 'other-server'}]
