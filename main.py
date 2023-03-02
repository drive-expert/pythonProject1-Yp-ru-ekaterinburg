import requests
from lxml import html
import csv
import json
from bs4 import BeautifulSoup
from json import JSONDecodeError

import  re
#import pandas as pd

city = 'ekaterinburg'
url = f'https://{city}.yp.ru'
head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
user_agent_val = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'

link_mass = []
link_massPRE = []
def replaceIT(sss):
    print(sss)
    a = pre_link_mass_create[link_orgPRE]
    print(a)
    return a
def multiple_replace(tel_str):
    replace_values = {"+7": "8", "(": "", ")":"", "-":"", " ":"", "tel:":""}

    for i5, j5 in replace_values.items():
        tel_str = tel_str.replace(i5, j5)
    return tel_str
def int_links(final_url):
    response = requests.get(final_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a')]
    to_extract = ["twitter.com", "mailto:"]
    social_links = []
    linkOLD =''
    for link in links:
        for social in to_extract:
            if link and social in link:
                if link != 'mailto:info@yp.ru':
                    if link != 'mailto:dbsale@yp.ru':
                        if link !=linkOLD:
                            social_links.append(re.sub('mailto:', '', link))
                            linkOLD = link
    return (social_links)

def vk_links(f_url):
    responseVK = requests.get(f_url)
    soup = BeautifulSoup(responseVK.content, 'html.parser')
    linksVK = [a.get('href') for a in soup.find_all('a')]
    to_extract_VK = ["vk.com"]
    social_linksVK = []
    linkOLD = ''
    for linkVK in linksVK:
        for socialVK in to_extract_VK:
            if linkVK and socialVK in linkVK:
                if linkVK != 'https://vk.com/yp_russia':
                    social_linksVK.append(linkVK)
                    linkOLD = linkVK

    return(social_linksVK)

def tel_link_create(link_now,id):
    url = 'https://www.yp.ru/ajax/GetPhoneByContactId'
    head = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    parser = "html.parser"

    payload = {'refer':str(link_now),
               'contact_id':id.split(id[:6])[1],
               'path':'/ajax/GetPhoneByContactId',
               }
    req = requests.post(url, headers=head, data = payload)
    #soup = BeautifulSoup(req.text, parser)
    ddd = req.content
    return ddd.decode("utf-8")
def title_tag(org_link):
    r = requests.get(org_link, headers=head)
    soup = BeautifulSoup(r.content, features="lxml")
    title = soup.title.string
    meta = soup.find_all('meta')

    for tag in meta:
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description', 'keywords']:
            na = re.search(r"[\w']+", tag.attrs['content'])[0]
    return na

def pre_link_mass_create():
    responsePRE = requests.get(url, headers=headers)
    divmass = [1,5,15,16,19,22] #номер div в списке рубрик
    amass = range(1,300) #количество подразделов в рубрике
    chPRE = 1
    print('РАБОТАЕТ ФУНКЦИЯ ple_link_mass_create')
    if responsePRE.status_code == 200:
        treePRE = html.fromstring(responsePRE.text)
        for dPre in divmass:
            for uPre in amass:
                link_orgPRE = treePRE.xpath(f'//*[@id="rb"]/div/div[{dPre}]/div/a[{uPre}]/@href')

                if len(link_orgPRE) > 0:
                    #print(f'строка:{uPre},раздел:{dPre}')
                    print(f'{chPRE}>>>>https://{city}.yp.ru{link_orgPRE[0]}')
                    link_massPRE.append(f'https://{city}.yp.ru{link_orgPRE[0]}')
                    chPRE=chPRE+1
    print(link_massPRE)
    print('PRE_LINK_MASS_CREATE = FINISH')
    return (link_massPRE)

def link_mass_create(link_mass_PRE):
    ii = 1
    print('РАБОТАЕТ ФУНКЦИЯ link_mass_create')
    max_page = range(1,300) #число страниц всего
    max_string = range(2,22) #число компаний на странице
    for pre_url in link_mass_PRE:
        response0 = requests.get(pre_url, headers=headers)
        print(f'Обрабатывается ссылка: {ii} >> {pre_url}')
        if response0.status_code == 200:
            tree0 = html.fromstring(response0.text)
            for u in max_string:
                link_org0 = tree0.xpath(f'///html/body/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[{u}]/div/div/div[1]/div/h2/a/@href')

                if len(link_org0) > 0:
                    if str(link_org0) != f'https://{city}.yp.ru/detail/id/bilain_3625195/':
                        #print()
                        #print(f'В строке {u} ПЕРВОЙ страницы ссылка >>>>https://www.yp.ru{link_org0[0]}')
                        link_mass.append(f'https://{city}.yp.ru{link_org0[0]}')
        for i in max_string:
            pre_url_n=f'{pre_url}page/{str(i)}/'
            #print()
            #print(f'Ссылка на {i} страницу:{pre_url_n}')

            response = requests.get(pre_url_n, headers = headers)
            chB = 1
            if response0.status_code == 200:
                tree = html.fromstring(response.text)
                for d in max_page: #число ссылок на второй и следующих страницах
                    link_org = tree.xpath(f'///html/body/div[2]/div/div/div[1]/div[2]/div[1]/div[1]/div[{d}]/div/div/div[1]/div/h2/a/@href')
                    if len(link_org) > 0:
                        if str(link_org) != f'https://{city}.yp.ru/detail/id/bilain_3625195/':
                            if  str(link_org) != f'https://{city}.yp.ruhttps://{city}.yp.ru/detail/id/bilain_3625195/':
                                #print(f'{chB}ссылка >>>>https://www.yp.ru{link_org[0]}')
                                link_mass.append(f'https://{city}.yp.ru{link_org[0]}')
                    chB = chB + 1
            ii = ii+1
    print('ФУНКЦИЯ link_mass_create FINISH')
    print(link_mass)
    return (link_mass)


def parse_link(link_org_n):
    ch = 1
    with open(f'yp-ru-{city}.csv', mode='w', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=","
                                 , lineterminator="\r")
        names = ["Наименование", "ИНН", "WhatsApp", "Телефон (офис)", "Телефон (мобильный)", "Сайт", "VK", "Email", "Адрес"]
        file_writer = csv.DictWriter(w_file, delimiter=",", lineterminator="\r", fieldnames=names)
        file_writer.writeheader()
        for n in link_org_n:
            if str(n) != f'https://{city}.yp.ruhttps://{city}.yp.ru/detail/id/bilain_3625195/':
                print(f'ОБРАБАТЫВАЕМ ССЫЛКУ {ch}:{str(n)}')
                check = requests.head(str(n))
                print(f'Ответ сервера:{str(check)}')
                if str(check) == '<Response [200]>':
                    response_n = requests.get(str(n), headers=head)
                    tree_n = html.fromstring(response_n.text)
                    org_wa=''
                    org_mob=''
                    org_vk=''
                    org_email = str(int_links(n))[1:-1].replace("'", "")
                    org_vk = str(vk_links(n))[1:-1].replace("'", "").replace(","," ")
                    for i in tree_n.xpath('/html/body/div[2]/div/div/div[2]/div[3]/div/div[1]/div/div[1]/p[1]/a/@id'):
                        id = i
                        org_tel = multiple_replace(tel_link_create(n,id))
                        if org_tel[1] == '9':
                            org_wa = f'https://wa.me/7{org_tel[1:11]}'
                            org_mob = f'7{org_tel[1:11]}'
                            org_tel = ''
                    if len(str(tree_n.xpath('//*[@id="utm"]/div[2]/div[1]/div/div/div[1]/h1/text()'))[1:-1].replace("'","")) > 0:
                        org_name = str(tree_n.xpath('//*[@id="utm"]/div[2]/div[1]/div/div/div[1]/h1/text()'))[1:-1].replace("'","")
                    else:
                        org_name = str(title_tag(n))
                    org_inn = str('000000000')
                    org_site = str(tree_n.xpath('//*[@id="contacts"]/div[1]/p[2]/a/text()'))[1:-1].replace("'","")
                    org_addr = str(str(tree_n.xpath('//*[@id="companyAddr"]/text()'))[1:-1].replace("'","")).replace(","," ")
                    #print(f'{ch}> Name:{str(org_name)}, INN{ch}: {str(org_inn)}, TelOffice{ch}:{str(org_tel)}, TelMob{ch}:{str(org_mob)},WA{ch}:{str(org_wa)}, Site{ch}:{str(org_site)}, VK{ch}:{str(org_vk)}, Email{ch}:{str(org_email)}, Addr{ch}:{str(org_addr)}')
                    if org_site != 'yprussia.turbo.site':
                        if org_tel != '88123095098':
                            if org_addr != '194100  Санкт-Петербург  Кантемировская улица  дом 37  офис 3.25В':
                                file_writer.writerow({"Наименование": str(org_name), "ИНН": str(org_inn),"WhatsApp": str(org_wa), "Телефон (офис)": str(org_tel), "Телефон (мобильный)": str(org_mob), "Сайт": str(org_site),"VK": str(org_vk), "Email": str(org_email),"Адрес": str(org_addr)})
                                print(f'{ch}> Name:{str(org_name)}, INN{ch}: {str(org_inn)}, TelOffice{ch}:{str(org_tel)}, TelMob{ch}:{str(org_mob)},WA{ch}:{str(org_wa)}, Site{ch}:{str(org_site)}, VK{ch}:{str(org_vk)}, Email{ch}:{str(org_email)}, Addr{ch}:{str(org_addr)}')
                                ch = ch + 1


pre_link_mass_create()
link_mass_create(link_massPRE)
parse_link(link_mass)