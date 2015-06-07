""" Netshow core module """
import netshowlib.netshowlib as nn

import os
import sys
import gettext


class UnableToFindProviderException(Exception):
    """
    Exception when Provider is not Found
    """
    pass


def run():
    """
    Executes ``run()`` function from netshow plugin identified
    from the provider check.
    """
    # set the LOCPATH to find locale files in the virtualenv instance or
    # system /usr/share/locale location. needed by gettext
    # for translation files.
    os.environ['LOCPATH'] = os.path.join(sys.prefix, 'share', 'locale')
    if os.environ.get('LANGUAGE') == 'C':
        os.environ['LANGUAGE'] = 'en'
    _ostype = nn.provider_check()
    if not _ostype:
        return UnableToFindProviderException
    import_str = 'netshow.%s.show' % _ostype
    nn.import_module(import_str).run()


def i18n_app(providername):
    """
    import this function at the top of each provider netshow component
    that has cli output  functions. Example

    from netshow.netshow import i18n_app as _
    """
    _translate = gettext.translation(providername,
                                     os.path.join(sys.prefix,
                                                  'share', 'locale'))
    return _translate.lgettext
