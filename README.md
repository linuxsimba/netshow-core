# netshow-core

Netshow is Network Abstraction Software. It is optimized to collect core networking data from devices that contain many network interfaces.

The netshow-core repository contains 2 packages:

### netshow-core-lib:
This is core library for retrieving network information from a  device and abstracting it into Python objects. Its core module is called ``netshowlib``. It contains a few high levels such as ``iface()``, ``system_summary()``, that when called, run a provider check function to retrieve the relevant core information about the interface or system.
A _provider_ is module that interacts with the base system and converts relevant network information into python objects. For example, the _Linux_ provider, when the netshow-core-lib ``iface()`` is called can retrieve network information like MTU, speed, IP address from device running a Linux kernel.

###netshow-core:

Netshow is responsible printing and analysing the information collected from the library component of netshow. *netshow-core* is the core component of this functionality and uses providers (_plugins_) to properly print and analyse gathered by the ``netshowlib`` component of the provider(_plugin_). For example, the ``print_iface`` wrapper class in the Linux netshow provider, is responsible for printing linux network information collected by the Linux provider ``netshowlib`` modules.

##Contributing

1. Fork it.
2. Create your feature branch (`git checkout -b my-new-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin my-new-feature`).
5. Create new Pull Request.

## License and Authors
Author:: Cumulus Networks Inc.

Copyright:: 2015 Cumulus Networks Inc.

![Cumulus icon](http://cumulusnetworks.com/static/cumulus/img/logo_2014.png)

### Cumulus Linux

Cumulus Linux is a software distribution that runs on top of industry standard
networking hardware. It enables the latest Linux applications and automation
tools on networking gear while delivering new levels of innovation and
ﬂexibility to the data center.

For further details please see: [cumulusnetworks.com](http://www.cumulusnetworks.com)

This project is licensed under the GNU General Public License, Version 2.0
