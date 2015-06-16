# pylint: disable=c0111
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from _gitversion import get_version
from setuptools import setup, find_packages
setup(
    name='netshow-core',
    version=get_version(),
    url="http://github.com/CumulusNetworks/netshow",
    description="Linux Network Troubleshooting Tool",
    author='Cumulus Networks',
    author_email='ce-ceng@cumulusnetworks.com',
    packages=find_packages(),
    namespace_packages=['netshow'],
    install_requires=[
        'setuptools',
        "netshow-core-lib"
    ],
    zip_safe=False,
    scripts=['bin/netshow'],
    data_files=[('share/bash-completion/completions/',
                ['data/completion/netshow'])],
    license='GPLv2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: System :: Networking',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
)