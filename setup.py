# pylint: disable=c0111
import versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = 'linux-netshow-lib/_version.py'
versioneer.versionfile_build = 'linux-netshow-lib/_version.py'
versioneer.tag_prefix = 'v'  # tags are like v1.2.0
versioneer.parentdir_prefix = '.'
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages
setup(
    name='linux-netshow-lib',
    url="http://github.com/skamithi/linux-netshow-lib",
    description="Python Library to Abstract Linux Networking Data",
    author='Stanley Karunditu',
    author_email='stanleyk@linuxsimba.com',
    packages=find_packages(),
    zip_safe=False,
    license='GPLv2',
    classifiers=[
        'Topic :: System :: Networking',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux'
    ],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
