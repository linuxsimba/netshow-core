""" Netshow core module """
import netshowlib.netshowlib as nn

import os
import sys


def run():
    """
    Executes ``run()`` function from netshow plugin identified
    from the provider check.
    """
    # set the LOCPATH to find locale files in the virtualenv instance or
    # system /usr/share/locale location. needed by flufl.i18n as its looking
    # for translation files.
    os.environ['LOCPATH'] = os.path.join(sys.prefix, 'share', 'locale')
    _ostype = nn.provider_check()
    import_str = 'netshow.%s.show' % _ostype
    nn.import_module(import_str).run()
