from ast import Break, Delete
from distutils import command
from distutils.log import ERROR
import json
from linecache import getline
from ntpath import join
from operator import delitem, truth
from pathlib import Path
from pickletools import unicodestring1
import random
from re import RegexFlag
from textwrap import indent
import time
import unicodedata
from xml.etree.ElementTree import tostring
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"liste_francais.txt")
url= "https://sutom.nocle.fr/#"
letter_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"letter.json")
word_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"word.json")

def init_json():
    
    if os.path.exists(letter_file) & os.path.exists(word_file):
        os.remove(letter_file)
        os.remove(word_file)

    letter_json = open(letter_file,"w")
    word_json = open(word_file, "w")

    listWord=[]
    listLetter=[]

    fieldsletter=['caractere','count','percentage','row','column']
    fieldsWord=['word','percentage','size']
    #INITIALISATION DU TABLEAU DE LETTRE
    ch = 'A'
    for i in range(26):
        dict2={}
        dict2[fieldsletter[0]] = ch
        dict2[fieldsletter[1]] = 0
        dict2[fieldsletter[2]] = 0
        listLetter.append(dict2)
        
        #rown
        if((ch=='A')|(ch=='Z')|(ch=='E')|(ch=='R')|(ch=='T')|(ch=='Y')|(ch=='U')|(ch=='I')|(ch=='O')|(ch=='P')):
            dict2[fieldsletter[3]]= 1
        elif((ch=='Q')|(ch=='S')|(ch=='D')|(ch=='F')|(ch=='G')|(ch=='H')|(ch=='J')|(ch=='K')|(ch=='L')|(ch=='M')):
            dict2[fieldsletter[3]]= 2
        else:
            dict2[fieldsletter[3]]= 3
        #column
        if((ch=='A')|(ch=='Q')):
            dict2[fieldsletter[4]]= 1
        if((ch=='Z')|(ch=='S')|(ch=='W')):
            dict2[fieldsletter[4]]= 2
        if((ch=='E')|(ch=='D')|(ch=='X')):
            dict2[fieldsletter[4]]= 3
        if((ch=='R')|(ch=='F')|(ch=='C')):
            dict2[fieldsletter[4]]= 4
        if((ch=='T')|(ch=='G')|(ch=='V')):
            dict2[fieldsletter[4]]= 5
        if((ch=='Y')|(ch=='H')|(ch=='B')):
            dict2[fieldsletter[4]]= 6
        if((ch=='U')|(ch=='J')|(ch=='N')):
            dict2[fieldsletter[4]]= 7
        if((ch=='I')|(ch=='K')):
            dict2[fieldsletter[4]]= 8
        if((ch=='O')|(ch=='L')):
            dict2[fieldsletter[4]]= 9
        if((ch=='P')|(ch=='M')):
            dict2[fieldsletter[4]]= 10
        ch = chr(ord(ch)+1)

    print("CHECK : CREATION DE LA LISTE DES LETTRES")

    #INITIALISATION DU TABLEAU DE MOTS ET MISE A JOUR DES LETTRES
    with open(filename,'r') as fh:
        countLetter = 0
        for line in fh:
            dict2 = {}
            wordnormal = line.replace("\n","") #unicodedata.normalize("NFD",''.join(line.rsplit("\n")))
            dict2[fieldsWord[0]]= wordnormal
            dict2[fieldsWord[1]]=0
            dict2[fieldsWord[2]] = len(line)-1
            listWord.append(dict2)
    


    # COMPTE DU NOMBRE D'APPARITION DE CHAQUE LETTRE

            for letter in line:
                countLetter+=1
                for caractere in listLetter:
                    if(caractere["caractere"] == letter):
                        caractere["count"] +=1
    # POURCENTAGE DES LETTRES
        for letter in listLetter:
            letter["percentage"] = letter["count"]/countLetter
        

        for word in listWord:
            add= 0
            for letter in word["word"]:
                for c in listLetter:
                    if letter == c["caractere"]:
                        add+=  c["percentage"]
            word["percentage"] = add/word["size"]

    print("CHECK : CREATION DU DICTIONNAIRE DE MOTS")

    json.dump(listWord,word_json)
    json.dump(listLetter,letter_json)
    word_json.close()
    letter_json.close()

# MAINTENANT QUE LA BDD EST INITIALISEE ON VA POUVOIR LA RECUPERER SOUS FORME DE DATA
def define_secret_word(data):
    alea = random.randrange(len(data))
    word = data[alea]
    print(word)
    return word

def update(data):

    with open(word_file,'w') as data_file:
       data = json.dump(data, data_file)

def getWordSize(word):
    return word["size"]

def getLetterByIndex(word,index):
    return word["word"][index]

def filterBySize(data,size):
    index =0
    for word in range(len(data)):
        if(getWordSize(data[index]) != size):
            del data[index]
        else:
            index+=1
    update(data)
    
def filterByLetterIndex(data,letter,index):
    i=0
    for word in range(len(data)):
        if(getLetterByIndex(data[i],index) != letter):
            del data[i]
        else:
            i+=1
    update(data)

def filterByLetterIndexRemove(data,letter,index):
    i=0
    for word in range(len(data)):
        if(getLetterByIndex(data[i],index) == letter):
            del data[i]
        else:
            i+=1
    update(data)

def getBestWord(data):
    bestword = data[0]
    for word in data:
        if(word["percentage"] > bestword["percentage"]):
            bestword = word
    return bestword

def findLetter(word,letter):
    for l in word["word"]:
        if(l==letter):
            return True
    return False

""" def getMask(words,wordd):
    masque=[]
    wordtempo=words["word"]
    for i in range(wordd["size"]):
        if(getLetterByIndex(words,i) == getLetterByIndex(wordd,i)):
            masque.append("V")
        else:
            found=False
            for j in range(len(wordtempo)):
                if(wordtempo[j] == getLetterByIndex(wordd,i)):
                    k = findLetter(words,j,wordtempo[j])
                    if(getLetterByIndex(words,k) != getLetterByIndex(wordd,k)):
                        wordtempo = wordtempo.replace(wordtempo[j],'',1)
                        masque.append("O")
                        found=True
                        break
            if not(found):
                masque.append("X")
    print(wordtempo)
    return masque """

def getMaskWeb(browser,size,line):
    mask=[]
    for letter in range(size):
        anal = browser.find_element_by_xpath('//*[@id="grille"]/table/tr['+ str(line) +']/td['+str(letter+1) +']')
        print(anal.text)
        classes = anal.get_attribute("class").split(" ")
        if classes[0] == 'bien-place':
            mask.append('V')
        elif classes[0] == 'mal-place':
            mask.append('O')
        elif classes[0] == 'non-trouve':
            mask.append('X')
    return mask


def deleteWord(data,words):
    index=0
    for word in data:
        if(data[index]["word"]==words["word"]):
            del data[index]
        else:
            index+=1
    update(data)

def filterByLetter(data,letter):
    index=0
    for word in data:
        if ((findLetter(data[index],letter))):
            del data[index]
        else:
            index+=1

def filterByLetterExist(data,letter):
    index=0
    for word in data:
        if ((findLetter(data[index],letter))):
            del data[index]
        else:
            index+=1
    




def launch_game(dataL,dataW):

    #OUVRE LE NAVIGATEUR SUR LA PAGE DEMANDEE
    browser = webdriver.Chrome()
    browser.get(url)    


    #SUPPRIME LE DIALOG D'ENTREE
    browser.find_element_by_xpath('//*[@id="panel-fenetre-bouton-fermeture"]').click()

    #init des variables
    nbTry = 0
    find = False
    maskV=[]

    #definition du mot secret
    #secret = define_secret_word(dataW)
    #size= getWordSize(secret)
    #firstLetter = getLetterByIndex(secret,0)
    #print(firstLetter)
    ####PASSAGE EN VERSION WEB

    time.sleep(2)
    firstLetter = browser.find_element_by_xpath('//*[@id="grille"]/table/tr[1]/td[1]').text
    secret = browser.find_element_by_xpath('//*[@id="grille"]/table/tr[1]').text
    secret = secret.replace(" ","")
    print(secret)
    size = len(secret)
    print(size)

    #MASQUE DE VICTOIRE
    for i in range(size):
        maskV.append("V")
    #premier filtrage
    print(len(dataW))
    filterBySize(dataW,size)
    print(len(dataW))
    filterByLetterIndex(dataW,firstLetter,0)
    print(len(dataW))
    

    while not(find):
        nbTry+=1
        
        wordCurrent = getBestWord(dataW)
        print(wordCurrent["word"])
        print(wordCurrent["percentage"])
        for letter in wordCurrent["word"]:
            for car in dataL:
                if car["caractere"] == letter:
                    browser.find_element_by_xpath('//*[@id="input-area"]/div['+ str(car["row"]) +']/div['+ str(car["column"]) +']').click()
        browser.find_element_by_xpath('//*[@id="input-area"]/div[3]/div[9]').click()
        time.sleep(3)

        #ANALYSE AND FILTER
        secret = browser.find_element_by_xpath('//*[@id="grille"]/table/tr['+ str(nbTry+1)+']').text
        secret = secret.replace(" ","")
        print(secret)
            
                
        mask = getMaskWeb(browser,size,nbTry)
        print(mask)
        if(maskV==mask):
            
            find = True
            print(wordCurrent)
        else: 
            print(len(dataW))
            #MENAGE
            for value in range(len(mask)):
                l = getLetterByIndex(wordCurrent,value)
                if mask[value] == "V":
                    filterByLetterIndex(dataW,l,value)
                    print(len(dataW))
                if mask[value] == "O":
                   #A MODIFIER
                    #filterByLetterExist(dataW,l)
                    filterByLetterIndexRemove(dataW,l,value)
                if mask[value] == "X":
                    filterByLetterIndexRemove(dataW,l,value)
                    remove= True
                    for letter in range(wordCurrent["size"]):
                        if ((l == getLetterByIndex(wordCurrent,letter)) & (mask[letter]!="X")):
                            remove = False        
                    if remove:
                        print(l)
                        filterByLetter(dataW,l)
                    
            deleteWord(dataW,wordCurrent)

    browser.find_element_by_xpath('//*[@id="fin-de-partie-panel-resume-bouton"]').click()

                            

    print(nbTry)
    return nbTry


def main():
    
    c=0
    nbTry=1
    for i in range(nbTry):
        
    
        init_json()

        #open jsons for read    
        letter_json = open(letter_file,"r")
        word_json = open(word_file, "r")

        dataWord = json.load(word_json)
        dataLetter = json.load(letter_json)

        c += launch_game(dataLetter,dataWord)



        #close jsons
        word_json.close()
        letter_json.close()
    print(c/nbTry)
    return c/nbTry

    
if __name__ == "__main__":
    main()

input('Press ENTER to exit')