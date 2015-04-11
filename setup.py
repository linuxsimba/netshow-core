# pylint: disable=c0111
from distutils.core import setup
from netshowlib import get_version

setup(
    name='linux-netshow-lib',
    version=get_version(),
    url="http://github.com/skamithi/linux-netshow-lib",
    description="Python Library to Abstract Linux Networking Data",
    author='Stanley Karunditu',
    author_email='stanleyk@cumulusnetworks.com',
    packages=['netshowlib'])
