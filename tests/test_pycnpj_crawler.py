from pycnpj_crawler import __version__
from pycnpj_crawler.states.ba import Bahia
from .util import get_response
import mock

keys = [
    "cnpj",
    "incricao_estadual"
]


def test_version():
    assert __version__ == '0.1.0'


def get_ba_response(*args):
    return get_response("ba")


@mock.patch.object(
    Bahia,
    '_get_cnpj_raw_data',
    new=get_ba_response
)
def test_ba_extraction():
    cnpj = mock.Mock()
    ba = Bahia()
    data = ba.get_cnpj_data(cnpj)
    print(data)
    for key in keys:
        assert key in data and data[key] is not None
