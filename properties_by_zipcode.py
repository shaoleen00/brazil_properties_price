from bs4 import BeautifulSoup
import requests
import json


def crawler(cep):
    header = {
        'User-agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.10'}
    lista = []
    url1 = 'https://glue-api.vivareal.com/v1/listings?addressCountry=BR&filterPricingInfoBusinessType=SALE&filter=address.zipCode%3A%22' + \
        str(cep)+'%22%20AND%20pricingInfos.businessType%3A%22SALE%22%20AND%20propertyType%3A%22UNIT%22%20'
    url2 = '&includeFields=addresses%2ClistingsLocation%2Csearch%2Curl%2Cexpansion%2C&size=100'
    url3 = '&from=%s&filterPropertyType=UNIT&q=&developmentsSize=5&__vt='
    for i in range(1, 9601, 100):
        url = (url1) + url2 + (url3 % ((i-1)))
        soup = str(BeautifulSoup(
            requests.get(url, headers=header).text,
            'html.parser'
        ))
        soup = json.loads(soup)
        if len(soup['search']['result']['listings']) == 0:
            print('CEP: %s Passo:%s Imoveis:0' % (cep, (i-1)))
            break
        if len(soup['search']['result']['listings']) >= 1:
            imoveis = len(soup['search']['result']['listings'])
            print('CEP: %s Passo:%s Imoveis:%s' % (cep, (i-1), imoveis))
            soup = soup['search']['result']['listings']
            for s in soup:
                id = s['url']['id']
                link = s['url']['link']['href']
                tipo = s['listing']['unitTypes'][0]
                try:
                    area_util = s['listing']['usableAreas'][0]
                except:
                    area_util = ''
                try:
                    area_total = s['listing']['totalAreas'][0]
                except:
                    area_total = ''
                try:
                    suites = s['listing']['suites'][0]
                except:
                    suites = '0'
                try:
                    banheiros = s['listing']['bathrooms'][0]
                except:
                    banheiros = '0'
                try:
                    quartos = s['listing']['bedrooms'][0]
                except:
                    quartos = '0'
                try:
                    preco = s['listing']['pricingInfos'][0]['price']
                except:
                    preco = ''
                try:
                    condominio = s['listing']['pricingInfos'][0]['monthlyCondoFee']
                except:
                    condominio = ''
                uf = s['listing']['address']['state']
                cidade = s['listing']['address']['city']
                bairro = s['listing']['address']['neighborhood']
                cep = s['listing']['address']['zipCode']
                lista_ = []
                lista_.append(id)
                lista_.append(link)
                lista_.append(tipo)
                lista_.append(area_util)
                lista_.append(area_total)
                lista_.append(suites)
                lista_.append(banheiros)
                lista_.append(quartos)
                lista_.append(preco)
                lista_.append(condominio)
                lista_.append(uf)
                lista_.append(cidade)
                lista_.append(bairro)
                lista_.append(cep)
                lista.append(tuple(lista_))
    return lista


lista_ceps = ['01001000', '04571090', '04671050']


for cep in lista_ceps:
    cont_error = 0
    while cont_error <= 3:
        try:
            resultado = crawler(cep)
            print(resultado)
            break
        except:
            cont_error += 1
            print('Realizando nova tentativa CEP: %s' % (cep))
            pass