# pylint: disable=c0111

from netshowlib import get_version
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
setup(
    name='linux-netshow-lib',
    version=get_version(),
    url="http://github.com/skamithi/linux-netshow-lib",
    description="Python Library to Abstract Linux Networking Data",
    author='Stanley Karunditu',
    author_email='stanleyk@linuxsimba.com',
    package_dir={'': 'netshowlib'},
    packages=find_packages('netshowlib'),
    zip_safe=False,
    license='GPLv2',
    classifiers=[
        'Topic :: System :: Networking',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ]
)
