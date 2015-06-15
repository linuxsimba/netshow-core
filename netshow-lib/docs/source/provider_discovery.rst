Provider Discovery
============

By default netshow-lib does not come with any providers. A list of providers can be found [TODO].


A provider can be a child of another provider, for example,
Gentoo provider is  a child of the Linux provider.  OS
discovery is managed by the :meth:`netshowlib.os_check()<netshowlib.netshowlib.os_check>` method.


It probes the ``$sys.prefix + 'usr/share/netshow-lib/discovery/`` for a list of
supported provider.  Then it calls
``netshowlib.<provider>.os_discovery`` and looks for the  ``name_and_priority()``
function, which returns a provider name and priority. For example ``{'Linux':
'0'}``

The provider discovery code picks the os type with the highest priority.

