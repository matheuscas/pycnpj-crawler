from requests_html import HTMLSession


class Bahia:

    URL_BASE = "https://www.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/consultaBa.asp"
    POST_URL = "https://www.sefaz.ba.gov.br/scripts/cadastro/cadastroBa/result.asp"

    selectors = {
        "cnpj": "#Table5 > tr > td > p:nth-child(1) > table > tr:nth-child(3) > td:nth-child(1)"
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

        def extract_cnpj_number(raw_cnpj): 
            return raw_cnpj.text.split(":")[1].strip()

        return {
            "cnpj": extract_cnpj_number(raw_cnpj)
        }
