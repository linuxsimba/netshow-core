# pylint: disable=c0111

from netshowlib import get_version
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
setup(
    name='linux-netshow-lib',
    version=get_version(),
    url="http://github.com/CumulusNetworks/netshow-lib",
    description="Python Library to Abstract Linux Networking Data",
    author='Cumulus Networks',
    author_email='ce-ceng@cumulusnetworks.com',
    packages=find_packages(),
    zip_safe=False,
    license='GPLv2',
    classifiers=[
        'Topic :: System :: Networking',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
    data_files=[('lib/linux.discover', 'var/lib/netshow/linux.discover')]
)
