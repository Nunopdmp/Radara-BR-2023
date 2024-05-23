from dados_jogador_time import *
import pandas as pd

def chute_por_jogo(df):
    column = df['adversario']
    if len(column) == 0:
        return []
    
    sequencias = []
    contador = 1
    valor_anterior = column[0]

    for valor in column[1:]:
        if valor == valor_anterior:
            contador += 1
        else:
            sequencias.append(( contador))
            valor_anterior = valor
            contador = 1
    
    sequencias.append((contador))  # Adicionar a última sequência
    return sum(sequencias)/len(sequencias)

def chute_ao_gol_por_jogo(df):
    column = df['adversario']
    shotType = df['shotType']
    if len(column) == 0:
        return []
    
    sequencias = []
    if shotType[0] == 'goal':
        contador = 1
    else:
        contador = 0
    for i in range(1, len(column)):
        if column[i] == column[i-1]:
            if shotType[i] == 'goal':
                contador += 1 
        else:
           sequencias.append((contador))
           contador = 0
    
    sequencias.append((contador))  # Adicionar a última sequência
    return sum(sequencias)/len(sequencias)

def sum_xg(df):
    soma = 0
    for x in df['xgot']:
        if pd.notna(x):  # Verifica se x não é NaN
            soma += x
    return soma

def gera_data_frame(lits_gabigol):
    df = pd.DataFrame(lits_gabigol)

    # Extraindo apenas o nome do jogador da chave 'name' dentro do dicionário 'player'
    df['player'] = df['player'].apply(lambda x: x['name'])

    # Ajustando os dados para as colunas desejadas
    df['x'] = df['playerCoordinates'].apply(lambda x: x['x'])
    df['y'] = df['playerCoordinates'].apply(lambda x: x['y'])

    df['block_x'] = df['blockCoordinates'].apply(lambda x: x['x'] if isinstance(x, dict) else None)
    df['block_y'] = df['blockCoordinates'].apply(lambda x: x['y'] if isinstance(x, dict) else None)

    # Selecionando as colunas desejadas
    return df[['time', 'player', 'x', 'y', 'block_x', 'block_y', 'shotType', 'isHome', 'xg', 'xgot', 'situation', 'adversario']]

def data_frame_radar(lits_gabigol):
    
    df = gera_data_frame(lits_gabigol)
    params = ['Gols', 'Chutes', 'Chutes ao gol', '%Chute ao gol', 'Cutes/90\'', 'Chutes ao Gol/90\'', 'Gol/Chute', 'Gol/Chute ao gol', 'xg', 'xgot']

    values_gabi =[]
    values_gabi.append(df['shotType'].value_counts().get('goal', 0))
    values_gabi.append(len(df['shotType']))
    values_gabi.append(df['shotType'].value_counts().get('save', 0) + (df['shotType'].value_counts().get('goal', 0)))
    values_gabi.append(df['shotType'].value_counts().get('save', 0)/len(df['shotType']))
    values_gabi.append(chute_por_jogo(df))
    values_gabi.append(chute_ao_gol_por_jogo(df))
    values_gabi.append(df['shotType'].value_counts().get('goal', 0)/len(df['shotType']))
    values_gabi.append(df['shotType'].value_counts().get('goal', 0)/((df['shotType'].value_counts().get('save', 0) + df['shotType'].value_counts().get('goal', 0))))
    values_gabi.append(sum(df['xg']))
    values_gabi.append(sum_xg(df))

    data_dict = {params[i]:values_gabi[i] for i in range(len(params))}
    data_dict['Player'] = df['player'][0]
    data_frame = pd.DataFrame([data_dict])
    return data_frame

def parametros_radar(lits_players):
    #add ranges to list of tuple pairs
    df = gera_data_frame(lits_players)
    ranges = []
    a_values = []
    b_values = []
    params = ['Gols', 'Chutes', 'Chutes ao gol', '%Chute ao gol', 'Cutes/90\'', 'Chutes ao Gol/90\'', 'Gol/Chute', 'Gol/Chute ao gol', 'xg', 'xgot']
    
    for x in params:
        a = min(df[params][x])
        a = a - (a*.25)
        
        b = max(df[params][x])
        b = b + (b*.25)
        
        ranges.append((a,b))
        
    for x in range(len(df['Player'])):
        if df['Player'][x] == 'Tammy Abraham':
            a_values = df.iloc[x].values.tolist()
        if df['Player'][x] == 'Timo Werner':
            b_values = df.iloc[x].values.tolist()
            
    a_values = a_values[1:]
    b_values = b_values[1:]

    values = [a_values,b_values]
