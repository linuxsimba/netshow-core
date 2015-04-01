Features
--------

Network Information Abstraction
===============================

Spanning tree, bond, switch discovery information and many other network
features are scattered throughout the linux filesystem.

For example, bond information is found in ``/proc/net/bonding`` and
``/sys/class/net``. netshow-lib aggregates information from these locations to
provide a comprenhensive view of the bond


* Interface details: link status, ip addresses (ipv4/ipv6), alias, mtu

* Bonds: Parses information found in ``/proc/net/bonding`` and other
  locations to provide comprehensive bond abstraction and summary information

* Counters: Depending on the OS, collects broadcast, multicast, unicast and
  total error counters.

* LLDP: Associate lldpctl output with interface objects

* Bridge Members:. Determine bridge member interface type, i.e is a
  bridge member an access port(single vlan) or a trunk (many vlans).

* Bridges: abstracts STP, IP info and bridge member information.
  Supports bridge interfaces with VLAN filtering support as well.
  Currently supports mstpd only. *(Support for the kernel STP soon)*

* Basic IP information: ARP and RP filter settings, IP addresses (ipv6/ipv4),
  DHCP settings, DHCP relay configuration.

* *Upcoming*
   * VXLan interface abstraction


OS Discovery
==============

``netshow-lib`` has an ``os_discovery`` module that is responsible for
determining the system ``netshow-lib`` is running on. It is called
by the interface discovery and feature cache discovery mechanisms.
By default the ``os-discovery`` module detects Linux. Plugins
to ``netshow-lib`` can include sub-modules for other operating system
or environments.


Interface Discovery
===================

``netshow-lib`` can perform interface discovery. The supported
interface types are

* Physical Interface

* Bridge Interface

* Bond Interface

* Bond Member Interface

* Sub Interface

* SVI


The library ``Iface`` instance  can also keeps track of whether these interface types have an IP
address, making it a **L3 interface**.

Or is a member of a bridge, making it a **L2 interface**.

L2 ports are further categorized into ports with a **single VLAN** *(access)*
or **multiple VLANs** *(trunk)* ports


