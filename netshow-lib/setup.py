# pylint: disable=c0111

from netshowlib._version import get_version
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass
import versioneer
from setuptools import setup, find_packages
setup(
    name='netshow-core-lib',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url="http://github.com/CumulusNetworks/netshow-lib",
    description="Netshow Core Library. Provides API for high level user apps and framework for providers",
    author='Cumulus Networks',
    author_email='ce-ceng@cumulusnetworks.com',
    packages=find_packages(),
    namespace_packages=['netshowlib'],
    zip_safe=False,
    license='GPLv2',
    classifiers=[
        'Topic :: System :: Networking',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
)
