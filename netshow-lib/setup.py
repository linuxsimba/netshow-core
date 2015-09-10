# pylint: disable=c0111
import os
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages
import io
# If installing this package from git, make sure to include 'gitversion' in
# requirements.txt
from version import __VERSION__

def read_contents(fname='README'):
    return io.open(os.path.join(os.path.dirname(__file__),
                                fname), encoding="utf-8").read()

setup(
    name='netshow-core-lib',
    version=__VERSION__,
    url="http://github.com/CumulusNetworks/netshow-core",
    description="Netshow Core Library. Provides high level user API for netshow providers",
    long_description=read_contents(),
    author='Cumulus Networks',
    author_email='ce-ceng@cumulusnetworks.com',
    packages=find_packages(),
    namespace_packages=['netshowlib'],
    zip_safe=False,
    license='GPLv2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: System :: Networking',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
)
