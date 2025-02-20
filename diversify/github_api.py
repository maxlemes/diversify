from datetime import datetime

import requests

from diversify.my_token import my_token


class GitHubAPI:
    def __init__(self):
        token = my_token()
        self.headers = {"Authorization": f"token {token}"}

    def obter_repositorio(self, usuario, repositorio):
        url = f"https://api.github.com/repos/{usuario}/{repositorio}"
        resposta = requests.get(url, headers=self.headers)
        return resposta.json() if resposta.status_code == 200 else None

    def verificar_limite(self):
        """Retorna o horário do próximo reset do limite de requisições da API do GitHub."""
        url = "https://api.github.com/rate_limit"
        resposta = requests.get(url, headers=self.headers)
        if resposta.status_code == 200:
            limites = resposta.json()
            reset_time = datetime.fromtimestamp(limites["rate"]["reset"])
            return f"O limite será restaurado em: {reset_time}"
        else:
            return f"Erro ao obter limite: {resposta.status_code}, {resposta.text}"
