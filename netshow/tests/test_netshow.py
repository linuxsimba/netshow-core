# pylint: disable=C0111
# pylint: disable=E0611
# pylint: disable=E1102
from netshow import netshow
import mock
import asserts
from asserts import assert_equals
from netshow.netshow import UnableToFindProviderException

import os
import sys
import pkg_resources


@mock.patch('netshowlib.netshowlib.provider_check')
@mock.patch('netshowlib.netshowlib.import_module')
def test_run(mock_import_module, mock_provider_check):
    mock_provider_check.return_value = 'linux'
    netshow.run()
    mock_import_module.assert_called_with('netshow.linux.show')


@mock.patch('netshowlib.netshowlib.provider_check')
@mock.patch('netshowlib.netshowlib.import_module')
@asserts.raises(UnableToFindProviderException)
def test_error_if_no_provider_found(mock_mod, mock_provider):
    mock_provider.return_value = ''
    netshow.run()


@mock.patch('netshowlib.netshowlib.provider_check')
@mock.patch('netshowlib.netshowlib.import_module')
def testing_of_env_vars_when_lang_is_c(mock_mod, mock_provider):
    mock_provider.return_value = 'linux'
    # test when os LANG is set to C set it by default to C
    os.environ['LANGUAGE'] = 'C'
    netshow.run()
    assert_equals(os.environ.get('LANGUAGE'), 'en')


@mock.patch('netshowlib.netshowlib.provider_check')
@mock.patch('netshowlib.netshowlib.import_module')
def testing_of_env_vars_when_lang_is_not_c(mock_mod, mock_provider):
    mock_provider.return_value = 'linux'
    # test when os LANG is set to C set it by default to C
    os.environ['LANGUAGE'] = 'es'
    netshow.run()
    assert_equals(os.environ.get('LANGUAGE'), 'es')


@mock.patch('netshowlib.netshowlib.provider_check')
@mock.patch('netshowlib.netshowlib.import_module')
def testing_of_env_vars_when_lang_is_not_c_or_en(mock_mod, mock_provider):
    mock_provider.return_value = 'linux'
    # test when os LANG is set to C set it by default to C
    os.environ['LOCPATH'] = ''
    os.environ['LANGUAGE'] = 'es'
    netshow.run()
    assert_equals(os.environ.get('LANGUAGE'), 'es')
    assert_equals(os.environ.get('LOCPATH'), (sys.prefix + '/share/locale'))


@mock.patch('netshow.netshow.gettext.translation')
def test_i18n_app(mock_gettext):
    provider = 'netshow-linux'
    translate_mock = mock.MagicMock()
    mock_gettext.return_value = translate_mock
    _result = netshow.i18n_app(provider)
    # check that it calls the right path to the .mo files

    install_location = pkg_resources.require('netshow-core-lib')[0].location
    mock_gettext.assert_called_with(provider, os.path.join(
        install_location, '..', '..', '..', 'share', 'locale'), fallback=True)
    # check that it calls the right gettext function. In this
    # case should be lgettext
    assert_equals(_result._mock_name, 'lgettext')
