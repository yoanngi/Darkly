import requests
import sys
import re

import time

url_base = "http://localhost:8042/.hidden/"
flag = None

def verif_result(html):
    """
        docstring for verif_result
        check result
    """
    if html.find("flag") > -1 or html.find("FLAG") > -1:
        return html
    if html.find("pass") > -1 or html.find("pwd") > -1:
        return html
    flag = re.findall('[0-9a-zA-Z]{31}', html)
    if len(flag) != 0:
        return html
    return None


def read_file(path):
    """
        docstring for read_file
        cherche le flag dans le fichier donnees par le path
    """
    global flag

    r3 = requests.get(path)
    res = verif_result(r3.text)
    if res != None:
        flag = path + " : " + res


def parcour_all(list_target, url):
    """
        docstring for parcour_all
        recursive
    """

    if list_target == None:
        list_target = []
        r = requests.get(url)
        verif_result(r.text)
        start = re.findall(r'"[0-9a-zA-Z]{26}', r.text)
        start = start + re.findall(r'README', r.text)
        for element in start:
            if element.find("README") > -1:
                read_file(url + element)
            else:
                list_target.append(str(url + element[1:] + "/"))
    for element in list_target:
        try:
            res = read_file(str(element) + "README")
        except:
            pass
    for element in list_target:
        r2 = requests.get(element)
        verif_result(r2.text)
        try:
            reponse = re.findall(r'"[0-9a-zA-Z]{26}', r2.text)
            reponse = reponse + re.findall(r'README', r2.text)
            for part in reponse:
                if part.find("README") > -1:
                    read_file(element + part)
                else:
                    parcour_all(None, element + part[1:] + "/")
            list_target.remove(element)
        except(Exception) as e:
            list_target.remove(element)

    return



parcour_all(None, url_base)
if flag == None:
    print("No result !")
else:
    print("%s" % flag)
sys.exit(0)
