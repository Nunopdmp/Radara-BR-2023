import requests
from bs4 import BeautifulSoup
import re

class MinerandoDados:
    def __init__(self, url):
        self.url = url
        response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'})
        
        soup = BeautifulSoup(response.text, 'html.parser')
        self.soup = soup

    def extrair_id(self):
        # Definir o padrão de expressão regular para encontrar o id na URL
        padrao = r'id:(\d+)'
        
        # Usar re.search para procurar o padrão na URL
        correspondencia = re.search(padrao, self.url)
        
        # Se encontrar uma correspondência, retornar o grupo capturado (o número de ID)
        if correspondencia:
            return correspondencia.group(1)
        else:
            return None

    def minerar(self):
        number_i = self.extrair_id()
        if not number_i:
            raise ValueError("ID não encontrado na URL")

        headers = {
            'accept': '*/*',
            'accept-language': 'pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            'referer': self.url,
            'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
            'x-requested-with': 'f7de0f',
        }

        session = requests.Session()
        api_url = f'https://www.sofascore.com/api/v1/event/{number_i}/shotmap'
        print(api_url)
        
        response = session.get(api_url, headers=headers)
        if response.status_code == 404:
            print("Recurso não encontrado. Verifique se o ID do evento está correto.")
            return None
        elif response.status_code != 200:
            print(f"Erro ao acessar a API: {response.status_code}")
            return None
        
        shots = response.json()
        lista = shots['shotmap']
        return lista

