netshow core
============

Netshow is Network Abstraction Software. It is optimized to collect core
networking data from devices that contain many network interfaces.

The netshow core respository has 2 main components:

netshow-core-lib:
-----------------

This is core library for retrieving network information from a device
and abstracting it into Python objects.

Its core module is called ``netshowlib``. It contains a few high levels
such as ``iface()`` and\ ``system_summary()``, that when called, this
calls a provider that retrieves the information from the system.

A *provider* is module that interacts with the base system and converts
relevant network information into python objects. For example, the
*Linux* provider, when the netshow-core-lib ``iface()`` is called, can
retrieve network information like MTU, speed, IP address from device
running a Linux kernel.

Example:
~~~~~~~~

With the Linux provider, retrieve details about the eth1 interface

::

    import netshowlib.netshowlib as nn
    eth1 = nn.iface('eth1')
    >>> eth1.ip_address.allentries
    [u'192.168.50.11/24']
    >>> eth1.lldp
    [{'adj_port': 'swp4', 'adj_mgmt_ip': '192.168.121.242', 'adj_hostname':
    'clswitch'}]
    >>> eth1.is_trunk()
    True
    >>> eth1.is_l3()
    True
    >>>

netshow-core:
-------------

Netshow is responsible printing and analysing the information collected
from the library component of netshow. *netshow-core* is the core
component of this functionality and uses providers (*plugins*) to
properly print and analyse gathered by the ``netshowlib`` component of
the provider(\ *plugin*). For example, the ``print_iface`` wrapper class
in the Linux netshow provider, is responsible for printing linux network
information collected by the Linux provider ``netshowlib`` modules.

Example
~~~~~~~

::

    $ netshow l3
       Name     Speed    MTU    Mode       Summary
    --  -------  -------  -----  -----      --------------------------------------------------------------------
    UP  br-mgmt  N/A      1500   Bridge/L3  IP: 192.168.20.11/24
                                            Untagged: veth2MAFSI, veth6HBXLS,veth7G1VTN, veth9LW4FV, vethADONKK
                                            Untagged: vethBAGOBS, vethBO11JN,vethF8GUCB, vethHEH94U, vethNGK2SR
                                            Untagged: vethNTRV1P, vethOEECMP,vethPUB40T, vethR69WUI, vethS7IYJR
                                            Untagged: vethU4MDPC, vethVPWMIY,vethWHB6XM
                                            Tagged: eth1
                                            802.1q Tag: 20
                                            STP: Disabled
    UP  eth0     N/A      1500   Access/L3  IP: 192.168.121.106/24(DHCP)
    UP  eth1     N/A      1500   Trunk/L2   Tagged: br-mgmt
    UP  lo       N/A      65536  Loopback   IP: 127.0.0.1/8, ::1/128
    UP  lxcbr0   N/A      1500   Bridge/L3  IP: 10.0.3.1/24
                                            Untagged: veth22SGDS, veth266GYO,veth29EVK1, veth3P9RFX, veth5394F7
                                            Untagged: veth9DS81W, vethATOKYC,vethFKCAWE, vethHS2PR0, vethIENOL2
                                            Untagged: vethQPW2WC, vethR24IIS,vethS37788, vethTMIEW7, vethTV9DFF
                                            Untagged: vethWF095K, vethYC5MCO,vethYEJ54L
                                            802.1q Tag: Untagged
                                            STP: Disabled

Contributing
------------

1. Fork it.
2. Create your feature branch (``git checkout -b my-new-feature``).
3. Commit your changes (``git commit -am 'Add some feature'``).
4. Push to the branch (``git push origin my-new-feature``).
5. Create new Pull Request.

License and Authors
-------------------

Author:: Cumulus Networks Inc.

Copyright:: 2015 Cumulus Networks Inc.

.. figure:: http://cumulusnetworks.com/static/cumulus/img/logo_2014.png
   :alt: Cumulus icon

Cumulus Linux
~~~~~~~~~~~~~

Cumulus Linux is a software distribution that runs on top of industry
standard networking hardware. It enables the latest Linux applications
and automation tools on networking gear while delivering new levels of
innovation and ﬂexibility to the data center.

For further details please see:
`cumulusnetworks.com <http://www.cumulusnetworks.com>`__

This project is licensed under the GNU General Public License, Version
2.0
