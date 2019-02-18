from bs4 import BeautifulSoup
import requests
import re
import telebot
import schedule
import time
import argparse

def get_channel_text(link):
    
    #Create scrapper
    r  = requests.get(link)

    data = r.text
    class_list = ["CABEZERA", "textosumario"]
    soup = BeautifulSoup(data, 'html.parser')

    text=''
    for row in soup.find_all('p',  class_=class_list):
         if row.get("class") == ['CABEZERA']:
              for li in row.find_all('a', href=True):
                 if li.string:
                     text=text+li.string.upper()+'\n'
         if row.get("class") == ['textosumario']:
              for li in row.find_all('a', href=True):
                 if li.string:
                    text=text+li.string+'\n'
    date=''
    for row in soup.find_all('p'):
        for row2 in row.find_all('b'):
            row3 = row2.find_all('span')[0]
            if row3.text:
                v = row3.text
                i = v.find('/')
                date1 = v[i - 2:i + 8]
                date=date+date1

    return str(date)+'\n\n'+text+'\n'+str(link)


def get_new_links():
    with open("urls.txt", 'a') as f:
        content = f.readlines()
        read_urls = [x.strip() for x in content]

    url = "portal.uned.es/portal/page?_pageid=93,64811283&_dad=portal&_schema=PORTAL"
    r = requests.get("http://" + url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    new_links=[]
    for row in soup.find_all('a'):
        link = row.get('href')
        match = re.search("^https://www2\\.uned\\.es/bici/Curso20\\d\\d-20\\d\\d/", link)
        if match:
            if link not in read_urls:
                new_links.append(link)
    return new_links


def save_links(new_links):
    with open("urls.txt", 'a+') as f:
        for l in new_links:
            f.write(l+'\n')


def broadcast(text, token):
    bot = telebot.TeleBot(token)
    bot.send_message(-1001452535069, text)


def job(token):
    links = get_new_links()
    for l in links:
        t = get_channel_text(l)
        broadcast(t, token)
    save_links(links)

def main():
    parser = argparse.ArgumentParser(description='Telegram token')
    parser.add_argument('token', type=str,
                        help='token')
    args = parser.parse_args()
    schedule.every().day.at("15:15").do(job, token=args.token)
    #schedule.every().minute.do(job, token=args.token)
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == "__main__":
        main()
