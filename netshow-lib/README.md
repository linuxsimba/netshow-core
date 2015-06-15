# netshow-lib

Abstracts network related information such as L3/L2 info, LLDP, Network services (ntp, dhcp, dhcrelay) into Iface Objects.

Core module for an infrastructure that abstracts network related information
such as L2 info, LLDP, Network services (dhcp, arp, ip) into Iface Objects.

It is designed to work with a linux device that is configured as a switch, but can work on a
server, but has a provider plugin architecture that can be expanded to other
operating systems.

## Installation

Not normally installed by itself. It is normally a requirement when install
a provider plugin.

But if you wish to do development, like when creating a new provider,
use ``pip`` to download a copy of this core module
```
pip install https://github.com/CumulusNetworks/netshow-lib/archive/master.tar.gz
```

Project will be available on PyPi soon.

## Usage

TODO: Write usage instructions

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Create a ``pyenv`` or [virtualenv](https://pypi.python.org/pypi/virtualenv/) instance.
Please try and develop using the latest stable Python3. Example:
```
$ virtualenv ~/netshow_dev /usr/local/bin/python3
```
4. Run ``setup.py develop to install development dependencies in virtualenv
   instance.
5. Write some cool code and _relevant nose tests too_
6. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


## Main Contributors

Stanley Karunditu [@skamithi](http://github.com/skamithi)

## License

GPLv2
