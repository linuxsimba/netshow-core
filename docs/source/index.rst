netshow-lib
======================================

.. toctree::
    :maxdepth: 1

    features.rst
    installation.rst
    development.rst
    provider_discovery.rst
    iface_discovery.rst
    api.rst
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

  from netshowlib import netshowlib

  # Create iface object
  iface = netshowlib.iface('eth1')

  print (netshowlib.os_check())
  >> 'linux'

  # print lldp information from linux system
  print(iface.lldp)
  >> [something]

Using an OS specific interface. No OS discovery

::

  from netshowlib import netshowlib

  iface = netshowlib.linux.Iface('swp10')

  print(iface.lldp)
  >> [something]


