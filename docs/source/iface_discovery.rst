Interface Discovery
====================

To create an interface with interface type discovery, call

.. code-block:: python

  import netshowlib

  eth1 = netshowlib.netshowlib.iface('eth1')


The mechanics behind this command is as follows

1. Method first performs :meth:`OS discovery<netshowlib.netshowlib.provider_check>` ::


2. Then calls the interface discovery function of the specific provider. For
   example, for the *linux* OS type, the call is :meth:`netshowlib.linux.iface.iface` ::


Probing Many Interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When probing many interfaces, it is better to first do Provider discovery,
and feature caching, then inform the interface discovery method what the OS type is.

.. code-block:: python

  from netshowlib import netshowlib as nl

  # perform Provider discovery, get os type
  os_type = nl.provider_check()

  # perform cache of features like ip addresses, lldp
  feature_cache = cache.cache()
  feature_cache.run()

  # generate a list of ifaces from eth0-8
  portlist = map(lambda x: 'eth' + str(x), range(0,9))
  porthash = {}

  # feed the os_type and cache into the interface discovery function
  for port in portlist:
    porthash[port] = nl.iface(port, os_type=os_type, cache=feature_cache)


