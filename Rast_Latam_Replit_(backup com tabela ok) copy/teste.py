
import pandas as pd

def gerar_excel():
    df = criar_dataframe()
    # Salve o DataFrame em um arquivo Excel temporário
    print(df)
    with pd.ExcelWriter('arquivo_temp.xlsx', engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Envie o arquivo Excel temporário como resposta
    #return send_file('arquivo_temp.xlsx', as_attachment=True)


def criar_dataframe():
    # Define uma lista de dicionários com dados fictícios
    dados = [{'NOME': 'Dato', 'SOBRENOME': "Carneiro", 'POSIÇÃO': "Atacante", "NÍVEL": 10},
             {'NOME': 'Dato', 'SOBRENOME': "Santos", 'POSIÇÃO': "Meio-campo", "NÍVEL": 10}]
    # Cria um DataFrame pandas a partir da lista de dicionários
    df = pd.DataFrame(dados)
    

    return df

gerar_excel()