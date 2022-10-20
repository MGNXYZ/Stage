#!/usr/bin/python
import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

from fileinput import close, filename
from hashlib import new
from operator import ne
from traceback import print_tb
from bs4 import BeautifulSoup
import requests, datetime
from lxml import etree
import re

# Adresse ip du control panel

firewalls_ip = [
 ''
]

date_1 = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")

# Token API palo alto

key = '' 

params = (
 ('type', 'export'),
 ('category', 'configuration'),
 ('key', key),
)


for hostname in firewalls_ip:

   print("Saving config for : %s" %hostname)
   url = "https://"+hostname+"/api/"
   
   response = requests.get(url, params=params, verify=False)
   
   xml_str = response.text
   root = etree.fromstring(xml_str)

fi = open("parse.txt", "a")
fi.write(xml_str)
fi.close

with open("parse.txt", "r") as f:
    file = f.read()

soup = BeautifulSoup(file, 'xml')

# Parse le tag <reserved> du fichier XML

reserved = str(soup.find_all('reserved'))

fixed = reserved.replace('<reserved><entry ', '').replace('</mac></entry><entry', '\n\n').replace('><mac>', ' mac= ').replace('</mac></entry></reserved>', '').replace('/><entry ', '\n\n').replace('/></reserved>,', '\n\n').replace('/></reserved>', '')

# Ne pas oublier de changer le chemin de sauvegarde du fichier au format .txt

f = open("reservation.txt", 'a')
print(fixed, file=f)
f.close()


# Ajoute les noms de vlan pour chaque adresse

with open('reservation.txt', 'r') as infile:
    data = infile.read()
final_list = []
for ind, val in enumerate(data.split('\n')):
    final_list.append(val)
   # if re.search('name="10.130.+', val) :
    #    final_list.insert(0, 'Tag 301 = Arbaud / ' +val + '\n')
    if re.search('name="10.13.2.+', val) :
        final_list.insert(0, 'Tag 302 = PtArc / ' +val + '\n')
    if re.search('name="10.13.3.+', val) :
        final_list.insert(0, 'Tag 303 = Lan CMS / ' +val + '\n')
    if re.search('name="10.13.4.+', val) :
        final_list.insert(0, 'Tag 304 = Inspection Academique PtArc / ' +val + '\n')
    if re.search('name="10.13.5.+', val) :
        final_list.insert(0, 'Tag 305 = Lauves / ' +val + '\n')
    if re.search('name="10.13.6.+', val) :
        final_list.insert(0, 'Tag 306 = Wallon / ' +val + '\n')
    if re.search('name="10.13.7.+', val) :
        final_list.insert(0, 'Tag 307 = StAndre / ' +val + '\n')
    if re.search('name="10.13.8.+', val) :
        final_list.insert(0, 'Tag 308 = Laurent-Jaures-Grassi / ' +val + '\n')
    if re.search('name="10.13.11.+', val) :
        final_list.insert(0, 'Tag 311 = Mauron-Roumanille-Serre / ' +val + '\n')
    if re.search('name="10.13.12.+', val) :
        final_list.insert(0, 'Tag 312 = Ferry / ' +val + '\n')
    if re.search('name="10.13.13.+', val) :
        final_list.insert(0, 'Tag 313 = Mistral / ' +val + '\n')
    if re.search('name="10.13.14.+', val) :
        final_list.insert(0, "Tag 314 = Isaac / " +val + '\n')
    if re.search('name="10.13.15.+', val) :
        final_list.insert(0, "Tag 315 = Veil / " +val + '\n')
    if re.search('name="10.13.16.+', val) :
        final_list.insert(0, "Tag 316 = Salier / " +val + '\n')
    if re.search('name="10.13.17.+', val) :
        final_list.insert(0, "Tag 317 = Pagnol / " +val + '\n')
    if re.search('name="10.13.18.+', val) :
        final_list.insert(0, "Tag 318 = Sextius / " +val + '\n' )
    if re.search('name="10.13.19.+', val) :
        final_list.insert(0, "Tag 319 = Floralies / " +val + '\n')
#    if re.search('name="10.13.100.+', val) :
#        final_list.insert(0, "Tag 400 = MJD / " +val + '\n')

# sauevgarde du fichier !!!Ajouter le chemin de sauvegarde!!!

with open('reservation.txt', 'w') as outfile:
    data      = outfile.write('\n'.join(final_list))
    outfile.close()

with open("reservation.txt", 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        fp.writelines(lines[:-797])


