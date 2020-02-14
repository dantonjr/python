# Atualizar o pip
#	python -m pip install --upgrade pip
#
# Instalar o BeautifulSoup
#	pip install beautifulsoup4
#
# Instalar o requests
#	pip install requests
#
# Página fonte
#	http://loteriasbr.com/site/home/?search=2018-11-02
#
# Danton Cavalcanti Franco Junior - falecom@dantonjr.com.br

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import csv
import re

arquivo = open('resultados.csv', 'w', newline = '')
gravaCSV = csv.writer(arquivo, delimiter = ';', doublequote = False, skipinitialspace = True)
gravaCSV.writerow(['Data', 'Jogo', '1 prêmio', '2 prêmio', '3 prêmio', '4 prêmio', '5 prêmio'])
dataInicial = datetime(2018, 11, 1)

for dias in range(int((datetime.now() - dataInicial).days)):
    dataFim = dataInicial + timedelta(dias)
    url = "https://loteriasbr.com/site/home/?search=%s" % dataFim.strftime('%Y-%m-%d')
    pagina = requests.get(url)

    soup = BeautifulSoup(pagina.content, 'html.parser')
    print(url, "Status:", pagina.status_code)

    divJogos = soup.findAll('div', class_='panel quadro-jogo')

    for jogo in divJogos:
        nomeCheio = jogo.findAll('div')
        nomeJogo = nomeCheio[0].get_text()
        nomeJogo = nomeJogo[1:nomeJogo.find(' ')]
        if not re.search(".*(PT|FD|COR).*", nomeJogo):
            continue

        resultados = jogo.findAll('span', class_='pull-right')
        gravaCSV.writerow([dataFim.strftime('%d/%m/%Y'), nomeJogo, resultados[0].get_text().replace('.', ''), resultados[1].get_text().replace('.', ''), resultados[2].get_text().replace('.', ''), resultados[3].get_text().replace('.', ''), resultados[4].get_text().replace('.', '')])

arquivo.close()
print("fim")
