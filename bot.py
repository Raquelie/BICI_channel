from bs4 import BeautifulSoup
import requests
import re
import telebot
import schedule
import time


def get_channel_text(link):

    r  = requests.get(link)

    data = r.text
    class_list = ["CABEZERA", "textosumario"]
    soup = BeautifulSoup(data)

    text=''
    for row in soup.find_all('p',  class_=class_list):
         if row.get("class") == ['CABEZERA']:
              for link in row.find_all('a', href=True):
                 if link.string:
                     text=text+link.string.upper()+'\n'
         if row.get("class") == ['textosumario']:
              for link in row.find_all('a', href=True):
                 if link.string:
                    text=text+link.string+'\n'
    return text+'\n'+str(link)


def get_new_links():
    with open("urls.txt") as f:
        content = f.readlines()
        read_urls = [x.strip() for x in content]

    url = "portal.uned.es/portal/page?_pageid=93,64811283&_dad=portal&_schema=PORTAL"
    r = requests.get("http://" + url)
    data = r.text
    soup = BeautifulSoup(data)

    new_links=[]
    for row in soup.find_all('a'):
        link = row.get('href')
        match = re.search("^https://www2\\.uned\\.es/bici/Curso20\\d\\d-20\\d\\d/", link)
        if match:
            if link not in read_urls:
                new_links.append(link)
    return new_links


def save_links(new_links):
    with open("urls.txt", 'w') as f:
        for l in new_links:
            f.write(l+'\n')


def broadcast(text):
    bot = telebot.TeleBot(TOKEN)
    #bot.send_message(-1001452535069, text)


def job():
    links = get_new_links()
    for l in links:
        t = get_channel_text(l)
        broadcast(t)
    save_links(links)

def main():
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)



if __name__ == "__main__":
        main()