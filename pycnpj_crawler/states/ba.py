from requests_html import HTMLSession


class Bahia:

    URL_BASE = "https://www.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/consultaBa.asp"
    POST_URL = "https://www.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/result.asp"

    selectors = {
        "cnpj": "#Table5 > tr > td > p:nth-child(1) > table > tr:nth-child(3) > td:nth-child(1)",
        "incricao_estadual": "#Table5 > tr > td > p:nth-child(1) > table > tr:nth-child(3)  > td:nth-child(2)",
        "razao_social": "#Table5 > tr > td > p:nth-child(1) > table > tr:nth-child(4)  > td:nth-child(1)"
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
        return session.post(self.POST_URL, data=payload)

    def get_cnpj_data(self, cnpj):
        html = self._get_cnpj_raw_data(cnpj).html
        raw_cnpj = html.find(self.selectors["cnpj"], first=True)
        raw_incricao_estadual = html.find(
            self.selectors["incricao_estadual"],
            first=True
        )
        raw_razao_social = html.find(
            self.selectors["razao_social"], 
            first=True
        )

        def get_value(raw_value):
            no_special_char = raw_value.text.replace("\xa0", " ")
            value = no_special_char.split(":")[1].strip()
            return value

        return {
            "cnpj": get_value(raw_cnpj),
            "incricao_estadual": get_value(raw_incricao_estadual),
            "razao_social": get_value(raw_razao_social)
        }
