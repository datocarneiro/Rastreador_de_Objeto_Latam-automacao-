import time
from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from flask import Flask, render_template, jsonify, request
from openpyxl import load_workbook
from werkzeug.utils import secure_filename
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

##########################################################################
'''
# para rodar no replit usar essas configuraçõa
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.headless = False  # Executar o Chrome de forma oculta

driver = webdriver.Chrome(options=options)
'''
#############################################################################

# para rodar local usar essa configuração aqui
from webdriver_manager.chrome import ChromeDriverManager

servico = Service(ChromeDriverManager().install())

opcoes = Options()
opcoes.headless = True  # modo off ou não
driver = webdriver.Chrome(service=servico, options=opcoes)



# Inicialização do aplicativo Flask
app = Flask(__name__)

lista_pendentes = []  # Variável global para armazenar a lista


@app.route('/')
def index():
  return render_template('index.html', pendentes=lista_pendentes)


@app.route('/', methods=['POST'])
def preparar_dados_planilha():
  global lista_pendentes  # Acessando a variável global
  file = request.files['file']

  # Solicitar ao usuário que escolha o nome de saída para o arquivo DataFrame
  # arquivo_saida = secure_filename(file.filename).replace('.xlsx', '_modificado.xlsx')

  if not file.filename.endswith('.xlsx'):
    return "Por favor, selecione um arquivo Excel (.xlsx)"

  # Carregar planilha
  planilha = load_workbook(file)
  aba_ativa = planilha.active

  # LER A PLANILHA, E CRIAR UMA LISTA SOMENTE COM AS ENTREGAS DIFERENTE DE "ENTREGUE"
  lista_pendentes = []
  for coluna_a, coluna_c, coluna_d in zip(aba_ativa["A"][1:],
                                          aba_ativa["C"][1:],
                                          aba_ativa["D"][1:]):
    # se os dados da coluna "D(status)" forem diferente de "Entregue", adicione(append) à lista os dados da coluna "C(AWB)".
    if coluna_d.value != 'ENTREGUE':
      if coluna_c.value is not None:
        lista_pendentes.append(coluna_c.value)

  print("=" * 150)
  print(f'As pendente de entrega são: {lista_pendentes}')
  print("=" * 150)

  statuses, datas = capturar_status_pendentes()
  capturas = []  # Lista para armazenar os valores de captura

  for awb, status, data in zip(lista_pendentes, statuses, datas):
    captura = f'{awb}    ,{status}    ,{data}'
    capturas.append(captura)  # Adicionar a captura à lista

  return render_template('index.html',
                         pendentes=lista_pendentes,
                         statuses=statuses,
                         datas=datas,
                         capturas=capturas)


# FUNÇÃO PARA CONSULTAR STATUS DE RASTREAMENTO NO SITE DA LATAM
def captura_status(awb):
  driver.get(
    f"https://www.latamcargo.com/en/trackshipment?docNumber={awb}&docPrefix=957&soType=SO"
  )

  wait = WebDriverWait(driver, 30)  # Aumentar o tempo limite para 30 segundos

  try:
    status_evento = wait.until(
      EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[1]')))
    status = status_evento.text

    data_evento = wait.until(
      EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="statusTable"]/tbody/tr[1]/td[6]')))
    data = data_evento.text

    captura = f'dados capturados,AWB,{awb},STATUS,{status},DATA_EVENTO,{data}'
    print(captura)

    return status, data
  except TimeoutException:
    # Lidar com o erro de tempo limite
    status = "Erro de tempo limite"
    data = "Erro de tempo limite"
    print("Erro de tempo limite ao capturar os dados")
    return status, data


def capturar_status_pendentes():
  dados_rastreamento = []
  statuses = []  # Lista para armazenar os valores de status
  datas = []  # Lista para armazenar os valores de data

  for awb in lista_pendentes:
    status, data = captura_status(awb)
    dados_rastreamento.append({
      'AWB': awb,
      'STATUS': status,
      'DATA_EVENTO': data
    })
    statuses.append(status)  # Adicionar o status à lista
    datas.append(data)  # Adicionar a data à lista

  # df_rastreamento = pd.DataFrame(dados_rastreamento)

  return statuses, datas


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)
