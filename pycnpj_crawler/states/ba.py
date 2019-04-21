from requests_html import HTMLSession
from .crawling import wait_random_delay, get_random_user_agent
import unidecode


class Bahia:

    URL_BASE = "http://www.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/consultaBa.asp"
    POST_URL = "http://www.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/result.asp"

    selectors = {
        "cnpj": "#Table5 > tr > td > p:nth-child(1) > table > tr:nth-child(3) > td:nth-child(1)",
        "incricao_estadual": "#Table5 > tr > td > p:nth-child(1) > table > tr:nth-child(3)  > td:nth-child(2)",
        "razao_social": "#Table5 > tr > td > p:nth-child(1) > table > tr:nth-child(4)  > td:nth-child(1)",
        "nome_fantasia": "#Table5 > tr > td > p:nth-child(1) > table > tr:nth-child(5)  > td:nth-child(1)"
    }

    def _get_cnpj_raw_data(self, cnpj):
        session = HTMLSession()
        session.get(self.URL_BASE)
        payload = {
            "sefp": 1,
            "estado": "BA",
            "CGC": cnpj,
            "B1": "CNPJ++-%3E",
            "IE": ""
        }
        wait_random_delay()
        return session.post(
            self.POST_URL,
            data=payload,
            headers={
                'User-Agent': get_random_user_agent()
            })

    def get_cnpj_data(self, cnpj):
        html = self._get_cnpj_raw_data(cnpj).html

        def get_value(raw_value):
            no_special_char = raw_value.text.replace("\xa0", " ")
            value = no_special_char.split(":")[1].strip()
            return value

        def get_key_value_pair(raw_value):
            no_special_char = raw_value.replace("\xa0", " ")
            key_value = no_special_char.split(":")
            return (turn_to_key(key_value[0].strip()), key_value[1].strip())

        def turn_to_key(field_name):
            lower = field_name.lower()
            lower = lower.replace(" ", "_")
            lower = lower.replace("/", "_")
            lower = lower.replace("-", "")
            lower = unidecode.unidecode(lower)
            return lower

        def get_company_data_section():
            obj = dict()
            tds = html.find("#Table6")[0].text.split("\n")[2:]
            for td in tds:
                k, v = get_key_value_pair(td)
                obj[k] = v
            return obj

        def get_address_data_section():
            obj = dict()
            tds = html.find("#Table6")[1].text.split("\n")[2:]
            for td in tds:
                k, v = get_key_value_pair(td)
                obj[k] = v
            return obj

        def get_activities_data_section():
            atividades = html.find("#Table7")[0].text.split("\n")[2:]
            atividade_principal = atividades[1].split("-")
            atividade = {
                "principal": {
                    "id": atividade_principal[0],
                    "descricao": atividade_principal[1]
                }
            }
            return atividade

        try:
            result = {
                **get_company_data_section(),
                "endereco": get_address_data_section(),
                "atividades": get_activities_data_section()
            }
            return result
        except Exception:
            raise Exception("CNPJ não encontrado")
