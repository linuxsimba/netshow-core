""" Netshow core module """
import netshowlib.netshowlib as nn


def run():
    """
    Executes ``run()`` function from netshow plugin identified
    from the provider check.
    """
    _ostype = nn.provider_check()
    import_str = 'netshow.%s.show' % _ostype
    nn.import_module(import_str).run()
