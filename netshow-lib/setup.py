# pylint: disable=c0111
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from _gitversion import get_version
from setuptools import setup, find_packages

with open('README') as f:
    readme_content = f.read().strip()

setup(
    name='netshow-core-lib',
    version=get_version(),
    url="http://github.com/CumulusNetworks/netshow-lib",
    description="Netshow Core Library. Provides high level user API for lower level providers",
    long_description=readme_content,
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
