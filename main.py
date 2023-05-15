from classes import CoinGeckoAPI, TelegramBot
import locale
from datetime import datetime
from time import sleep
from config import settings


id_moeda = input('Qual o ID da moeda a ser rastreada? ')
valor_minimo = int(input('Qual o valor mínimo para iniciar o rastreamento? '))
valor_maximo = int(input('E o valor máximo? '))
locale.setlocale(locale.LC_ALL, 'pt_BR.URF-8')

api = CoinGeckoAPI(url_base='https://api.coingecko.com/api/v3/')
bot = TelegramBot(token=settings.TOKEN, chat_id=settings.CHAT_ID)

while True:

    # Verifica se a API está online
    if api.ping():
        print('API online')
        preco, atualizado_em = api.consulta_preco(id_moeda=id_moeda)
        print('Consulta realizada com sucesso!')

        data_hora = datetime.fromtimestamp(atualizado_em).strftime('%x às %X')
        mensagem = None

        if preco < valor_minimo:
            mensagem = f'*Cotação do Ethereum*: \n\t*Preço:* R$ {preco}' \
                       f'\n\t*Horário:* {data_hora}\n\t*Motivo:* Valor menor que o mínimo'

        elif preco < valor_maximo:
            mensagem = f'*Cotação do Ethereum*: \n\t*Preço:* R$ {preco}' \
                       f'\n\t*Horário:* {data_hora}\n\t*Motivo:* Valor maior que o mínimo'

        if mensagem:
            bot.envia_mensagem(texto_markdown=mensagem)

    else:
        print('API offline, tente novamente mais tarde')

    sleep(300)
