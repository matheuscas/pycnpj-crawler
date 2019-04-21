from pycnpj_crawler.states.util import load_state_class
from pycpfcnpj import cpfcnpj


def get_cnpj_data(cnpj, state="ba"):
    """
    Busca no site do estado os dados do CNPJ provido

    Args:
        cnpj (str): CNPJ, somente numeros, da empresa alvo
        state (str): Sigla do estado, em letras minusculas

    Returns:
        cnpj (obj)
    """

    valid = cpfcnpj.validate(cnpj)
    if (not valid):
        raise Exception("CNPJ inválido")
    state = load_state_class(state)
    return state().get_cnpj_data(cnpj)
