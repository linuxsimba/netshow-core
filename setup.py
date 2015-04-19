# pylint: disable=c0111

from netshow._version import get_version
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup, find_packages
setup(
    name='netshow',
    version=get_version(),
    url="http://github.com/CumulusNetworks/netshow",
    description="Linux Network Troubleshooting Tool",
    author='Cumulus Networks',
    author_email='ce-ceng@cumulusnetworks.com',
    packages=find_packages(),
    # activate this when project is opensourced and netshow-lib and netshow-linux-lib
    # are available on pypi.
    # install_requires=[
    #    "netshow-lib"
    #    "netshow-linux-lib"
    # ]
    zip_safe=False,
    license='GPLv2',
    classifiers=[
        'Topic :: System :: Networking',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
)
