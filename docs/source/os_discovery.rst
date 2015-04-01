OS Discovery
============

By default there is one OS type. That is Linux. It is possible to create other
OS types like FreeBSD, or heavens, even MS Windows one day.


An *OS type* can be a child of another type, for example,
Gentoo OS type is  a child of the Linux OS type.  OS
discovery is managed by the :meth:`netshowlib.os_check()<netshowlib.netshowlib.os_check>` method.


It probes the ``netshowlib/os_discovery/`` that
each have a ``check()`` function in it. The :meth:`netshowlib.os_check()<netshowlib.netshowlib.os_check>` method
goes through all the viable OS types defined in the
``netshowlib/os_discovery`` directory to determine the best match.


.. note:: By default the linux discovery checker ``netshowlib/os_discovery/linux.py`` is provided


For example, if the ``netshowlib/os_discovery`` directory contains the
following:

.. code-block:: shell

  netshowlib/os_discovery
  ├── debian.py
  ├── freebsd.py
  ├── __init__.py
  └── linux.py

When you run

.. code-block:: python

  import netshowlib
  netshowlib.netshowlib.os_check()
  >> 'debian'

It will call ``name_and_priority()`` function in each of the os_discovery files.

It will return a hash like so

.. code-block:: python

   {
     {   'linux': 0 },
     { 'debian': 1 }
   }

``os_check`` will then take the hash value with the *maximum value*
and return the os name as the prefered OS for this system.

So in this case, ``debian`` is the prefered OS.

The priorities for each OS type is statically assigned in the ``os_discovery``
files.





