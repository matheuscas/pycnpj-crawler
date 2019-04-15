from pycnpj_crawler import __version__, crawler
from pycnpj_crawler.states.ba import Bahia
from .util import get_response
import mock
import pytest
# import pprint

keys = [
    "cnpj",
    "inscricao_estadual",
    "razao_social",
    "nome_fantasia",
    "razao_social",
    "endereco",
    "atividades"
]

address_keys = [
    "numero",
    "complemento",
    "bairro_distrito",
    "cep",
    "municipio",
    "uf",
    "telefone",
    "email",
    "referencia"
]

activities_keys = [
    "principal"
]


def test_version():
    assert __version__ == '0.3.0'


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
    # pprint.pprint(data)
    for key in keys:
        assert key in list(data.keys())
        assert data[key] is not None

    for key in address_keys:
        assert key in list(data["endereco"].keys())
        assert data["endereco"][key] is not None

    for key in activities_keys:
        assert key in list(data["atividades"].keys())
        assert data["atividades"][key] is not None


def test_unavailable_state():
    cnpj = "39346861005716"
    state = "bb"
    error_msg = f"No module named 'pycnpj_crawler.states.{state}'"
    with pytest.raises(ModuleNotFoundError, match=error_msg):
        crawler.get_cnpj_data(cnpj, state)
