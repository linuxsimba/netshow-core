# pylint: disable=C0111
# pylint: disable=E0611
from netshow import netshow
import mock


@mock.patch('netshowlib.netshowlib.provider_check')
@mock.patch('netshowlib.netshowlib.import_module')
def test_run(mock_import_module, mock_provider_check):
    mock_provider_check.return_value = 'linux'
    netshow.run()
    mock_import_module.assert_called_with('netshow.linux.show')
