from pycnpj_crawler import __version__
from pycnpj_crawler.states.ba import Bahia
from .util import get_response
import mock
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
