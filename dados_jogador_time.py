from minerador_dados import MinerandoDados
import unicodedata
import re


def remover_acentos(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))


def time2(site,time):

# Expressão regular para capturar a parte após "sofscore.com/" até a próxima "/"
    match = re.search(r'sofascore\.com/([^/]+)', site)

    if match:
        resultado = match.group(1)
        
        # Removendo o time especificado da string resultado
        if time in resultado:
            resultado = resultado.replace(time, '').replace('--', '-')
            # Remover o traço inicial ou final, caso existam
            resultado = resultado.strip('-')
        else:
            resultado = 'N/A'
    return resultado

def dados_jogador(arquivo_sites, time, jogador):
    # abrir arquivo com a lista de sites
    lista_de_sites = []
    # time recebe o nome informado sem acentos e troca espaços por -
    time = remover_acentos(time).replace(" ", "-").lower()
    
    with open(arquivo_sites, 'r') as arquivo:
        linhas = arquivo.readlines()
        # filtrar linhas que contenham o nome do time
        lista_de_sites = [linha.strip() for linha in linhas if time in linha]

    lista_dicionarios = []

    # usar laço for para minerar os dados de todos os sites na lista
    for site in lista_de_sites:
        # instanciar o minerador de dados e minerar os dados
        mineiro = MinerandoDados(site)
        dados = mineiro.minerar()
        for dici in dados:
            # acessar o dicionário do nome do jogador e separá-lo no dici_jogador
            if dici.get('player').get('name') == jogador:
                # salvar o dicionário em uma lista de dicionários
                dici['adversario'] = time2(site,time)
                lista_dicionarios.append(dici)
        
        # deletar o objeto criado
        del mineiro

    # retornar a lista de dicionários
    return lista_dicionarios, jogador

#print(dados_jogador('brasileirao_2023_links.txt', 'flamengo', 'Gabriel Barbosa'))
