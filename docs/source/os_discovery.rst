OS Discovery
============

By default there is one OS type. That is Linux. It is possible to create other
OS types like FreeBSD, or heavens, even MS Windows one day.


An *OS type* can be a child of another type, for example,
Gentoo OS type is  a child of the Linux OS type.  OS
discovery is managed by the :meth:`netshowlib.os_check()<netshowlib.netshowlib.os_check>` method.


It probes the ``$sys.prefix + 'var/lib/netshow/*.discover`` for a list of
supported OS types.  Then it calls
``netshowlib.<os_type>.os_discovery`` and looks for the  ``name_and_priority()``
function, which returns a os type name and priority. For example ``{'Linux':
'0'}``

The OS discovery code picks the os type with the highest priority.


.. note:: By default the core netshow module supports the 'linux' os type.
