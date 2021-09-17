import time
import requests
from bs4 import BeautifulSoup
from telegram_bot import telegram_bot_send_message


def tiraBarraEne(string):  # Retira o '\n' presente nos arquivos
    string_nova = ""
    for char in string:
        if char != '\n':
            string_nova += char
    return string_nova


def salvar_lista():
    arq = open('titulos.txt', 'w')
    for x in l_tit:
        arq.write(str(x) + '\n')
    arq.close()

    arq2 = open('precos.txt', 'w')
    for y in l_prec:
        arq2.write(str(y) + '\n')
    arq2.close()


l_tit = ['', '', '', '', '', '', '']  # arquivo com lista dos titulos anteriores
l_prec = ['', '', '', '', '', '', '']  # arquivo com lista dos precos anteriores

titulos = open("titulos.txt", "r")
dados_titulos = titulos.readlines()
titulos.close()

precos = open("precos.txt", "r")
dados_precos = precos.readlines()
precos.close()

for x in range(len(dados_titulos)):
    l_tit[x] = tiraBarraEne(dados_titulos[x])
    l_prec[x] = tiraBarraEne(dados_precos[x])

print("Títulos armazenados:", l_tit)
print("Preços armazenados:", l_prec)
print("\n"*2)

urlList = [
    'https://www.olx.com.br/brasil?q=dell%20optiplex%20micro&sf=1&op=2',  # optiplex micro
    'https://www.olx.com.br/brasil?q=dell%20optiplex%20mini&sf=1&op=2',  # optiplex mini
    'https://www.olx.com.br/brasil?q=thinkcentre&sp=1&op=2',  # thinkcentre
    'https://www.olx.com.br/brasil?q=prodesk&op=2',  # prodesk
    'https://www.olx.com.br/brasil?q=elitedesk&op=2', # elitedesk
    'https://pe.olx.com.br/grande-recife?q=iphone%2011%20128gb&op=2', #iphone 11 128gb
    'https://pe.olx.com.br/grande-recife?q=iphone%20128gb&op=2' ] #iphone 128gb

request_headers = {
    'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/50.0.2661.102 '
        'Safari/537.36 '
}

while True:
    print("Iniciando requisições ...")
    cont = 0
    titulo = ''
    preco = ''
    for url in urlList:
        results = requests.get(url, headers=request_headers)
        status_code = results

        # HTML parser
        soup = BeautifulSoup(results.content, "html.parser")

        results = soup.find(id="ad-list")  # Busca todos os anuncios listados
        product = results.find("li")  # Filtra pelo anuncio mais recente
        data_postagem = product.find("div",
                                     class_="wlwg1t-0 hWBHAm")  # Classe da Div no olx que contém a data de postagem

        if data_postagem is None:  # Bug no OLX de div repetida e em branco
            pass
        else:
            data_postagem = data_postagem.text.strip()

            dados = product.find_all("a")
            for link in dados:
                url = link["href"]
                titulo = link["title"]

            preco = product.find("div", class_="aoie8y-0 hRScWw").text.strip()  # Classe da Div que contém o preço

            # print("Titulo:", titulo)
            # print("Data da postagem:", data_postagem)
            # print("preço:", preco)
            # print("url:", url)

            # - Caso um novo anuncio tenha sido adicionado, o titulo e o preco irão mudar.
            # - A data de postagem muda automaticamente de acordo com a hora no sistema, por
            #   isso não estamos verificando esse valor.
            if (titulo != l_tit[cont]) or (preco != l_prec[cont]):
                # Caso detecte mudanca no titulo ou no preco
                print("Mudança detectada!")
                l_tit[cont] = titulo
                l_prec[cont] = preco
                salvar_lista()
                telegram_bot_send_message(titulo, data_postagem, preco, url)
            else:
                print("Nada mudou!")

        print(f'Requisição HTTP realizada para {url} e obteve o código de status {status_code} \n')
        time.sleep(3)
        cont += 1
    print("Aguardando 60s ...")
    time.sleep(60)  # Verifica a cada 60s
