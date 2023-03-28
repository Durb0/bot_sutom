from ast import Break, Delete
from distutils import command
from distutils.log import ERROR
from linecache import getline
from ntpath import join
from operator import delitem, truth
from pathlib import Path
from pickletools import unicodestring1
import random
from re import RegexFlag
from textwrap import indent
import time
from typing import KeysView
from xml.etree.ElementTree import tostring
import os
from pip import main
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import letter
import word

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),"liste_francais.txt")
url= "https://sutom.nocle.fr/#"
letter_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"letter.json")
word_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"word.json")
letters=[]
words=[]
word_to_find = None



#fonction qui ouvre filename et crée un Word pour chaque ligne
def get_words(filename,size_file,firstLetter_file): 
      words = []
      with open(filename) as f:
            for line in f:
                  #si la premiere lettre de la ligne est la meme que firstLetter_file et la taille de la ligne est egale à size_file
                  if line[0] == firstLetter_file and len(line)-1 == size_file:
                        words.append(word.Word(line.strip()))
      return words


#retourne une ligne aleatoire du fichier filename
def get_random_line(filename):
      with open(filename) as f:
            lines = f.readlines()
            return random.choice(lines)


#function who return longest word
def longest_word(words:list):
      longest = words[0]
      for word in words:
            if word.getSize() > longest.getSize():
                  longest = word
      return longest


#fonction qui cherche un mot aléatoire dans la liste words
def random_word(words:list):
      return random.choice(words)


#fonction qui supprime un mot de la liste words
def delete_word(words:list,word):
      ###
      # if word in words:
      #     if(len(words)< 100):
      #          word.print_word()
      #   del words[words.index(word)]
      if word in words:
            words.remove(word)

#function who delete all word with the letter l
def deleteAllWordsWithLetter(l:str,words:list):
      deleteList=[]
      processNo = 0
      for word in words:
            #if word.checkLetter(l) > -1:
            for letter in word.word:
                  if letter == l:
                        deleteList.insert(0,processNo)
                        break
            processNo+=1
      if len(deleteList) > 0:
            for i in deleteList:
                  del words[i]

#function who delete all words without letter l
def deleteAllWordsWithoutLetter(l,words:list):
      deleteList=[]
      processNo = 0
      for word in words:
            if word.checkLetter(l) == -1:
                  deleteList.insert(0,processNo)
            processNo+=1
      if len(deleteList) > 0:
            for i in deleteList:
                  del words[i]

def deleteAllWordsWithLetterPosition(letter:str,words:list,pos:int):
      deleteList=[]
      processNo = 0
      for word in words:
            if word.getLetter(pos) == letter:
                  deleteList.insert(0,processNo)
            processNo += 1
      if len(deleteList) > 0:
            for i in deleteList:
                  del words[i]

#fonction qui supprime tout les mots qui n'ont pas la meme lettre à la position pos
def deleteAllWordsWithoutLetterPosition(letter:str,words:list,pos:int):
      deleteList=[]
      processNo = 0
      for word in words:
            if word.word[pos] != letter:
                  deleteList.insert(0,processNo)
            processNo += 1
      if len(deleteList) > 0:
            for i in deleteList:
                  del words[i]

#function who delete all words with not the size s
def deleteAllWordsWithSize(s:int,words:list):
      for word in words:
            if word.getSize() != s:
                  delete_word(words,word)

#function who return  the word with the better percent
def best_word(words:list):
      if len(words) == 0:
                  print("Aucun mot trouvé")
                  return None
      best = words[0]
      for word in words:
                  if word.getPercent() > best.getPercent():
                        best = word
      return best

################
# ABOUTE LETTERS #
################

#function who create a list of each letter of the alphabet
# and return it
def create_letters():
      letters = []
      for i in range(26):
                  #la lettre doit être en majuscule
                  letters.append(letter.Letter(chr(i+65)))
      return letters 

#fonction qui applique add_letter à chaque mot
def add_letters(words:list,letters:list):
      for word in words:
                  for i in range(word.getSize()):
                        findLetter(letters,word.word[i]).add(i)

#fonction qui affiche toutes les lettres en format json
def print_letters(letters:list):
      for letter in letters:
                  letter.print_letter()


def findLetter(letters:list,c:str):
      for letter in letters:
                  if letter.isLetter(c):
                        return letter
      return None

#fonction qui cacule le pourcentage de chaque mot
def calculate_percents(words:list,letters:list):
      for word in words:
                  word.calculatePercent(letters)

def initiatilisationTabs(words,letters,size_file,firstLetter_file):
      words = get_words(filename,size_file,firstLetter_file)
      add_letters(words,letters)
      for letter in letters:
            #si la lettre est une voyelle
            if letter.isVowel():
                  #on applique la fonction addPositionsPercent
                  letter.addPositionsPercent()
      calculate_percents(words,letters)
      return words


#fonction qui genere le masque de la recherche
#retourne un tableau
#"V" si la lettre est dans la meme position
#"O" si la lettre est dans une autre position
#"X" si la lettre n'est pas dans le mot
def getMask(word,word_to_find):
            mask = ["" for i in range(word.getSize())]
            for i in range(word.getSize()):
                  if word.getLetter(i) == word_to_find.getLetter(i):
                        mask[i] = "V"
            #si la lettre est dans le mot et qu'elle est dans une autre position et que le mask est vide
            for i in range(word.getSize()):
                  #si le masque a i est vide et que la lettre est dans le mot
                  if mask[i] == "":
                        for j in range(word.getSize()):
                              if word.getLetter(i) == word_to_find.getLetter(j) and (mask[j] != "V"):
                                    mask[i] = "O"
                                    break
                        if mask[i] == "":
                              mask[i] = "X"
            return mask

def getMaskWeb(browser,size,line):
      mask=[]
      for letter in range(size):
            #anal = browser.find_element_by_xpath('//*[@id="grille"]/table/tr['+ str(line) +']/td['+str(letter+1) +']')
            anal = browser.find_element(By.XPATH, '//*[@id="grille"]/table/tr['+ str(line) +']/td['+str(letter+1) +']')
            classes = anal.get_attribute("class").split(" ")
            if classes[0] == 'bien-place':
                  mask.append('V')
            elif classes[0] == 'mal-place':
                  mask.append('O')
            elif classes[0] == 'non-trouve':
                  mask.append('X')
      return mask

def checkMask(mask):
      for i in mask:
            if i != "V":
                  return False
      return True

def filter_words(words,mask,best):
      print(best.word)
      for i in range(best.getSize()):
            letter = best.getLetter(i)
            if mask[i] == "V":
                              #supprime tout les mots qui n'ont pas la lettre
                  deleteAllWordsWithoutLetterPosition(letter,words,i)
            elif mask[i]  == "O":
                              #supprime tout les mots qui on la lettre dans la meme position
                  deleteAllWordsWithLetterPosition(letter,words,i)
                  deleteAllWordsWithoutLetter(letter,words)
            elif mask[i] == "X":
                  #si O ou V de la lettre n'est pas dans le masque
                  #supprime tout les mots qui ont la lettre
                  is_other_position = False
                  for j in range(best.getSize()):
                        if (mask[j] == "V" or mask[j]=="O") and letter == best.getLetter(j):                         
                              deleteAllWordsWithoutLetterPosition(letter,words,j)
                              is_other_position = True
                              break
                  if  not is_other_position:
                        print("suppression de la lettre " + letter)
                        deleteAllWordsWithLetter(letter,words)

      #si le best existe toujours on le supprime
      if best in words:
            delete_word(words,best)
      
def ecritMot(browser,word,letters):
      for i in word.word:
            #recupère la lettre
            letter = findLetter(letters,i)
            #browser.find_element_by_xpath('//*[@id="input-area"]/div['+ str(letter.row) +']/div['+ str(letter.column)+']').click()
            browser.find_element(By.XPATH,'//*[@id="input-area"]/div['+ str(letter.row) +']/div['+ str(letter.column)+']').click()
      browser.find_element(By.XPATH,'//*[@id="input-area"]/div[3]/div[10]').click()
      time.sleep(3)

def find_word(words,word_to_find):
      for word in words:
            if word.word == word_to_find:
                  print("mot trouvé")
                  return word
      return None


def game(browser):
      letters = create_letters()
      words=[]

      ######
      # POUR TEST
      ######

      #line = get_random_line(filename) 
      #retire le dernier caractère de line
      #line = line[:-1]
      #print("Mot à trouver : ",line)
      #size_file = len(line)
      #firstLetter_file = line[0]

      ######
      # POUR SUTOM
      ######
      firstLetter_file = WebDriverWait( browser,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="grille"]/table/tr[1]/td[1]'))).text
      print("Premiere lettre du mot : ",firstLetter_file)
      word_to_find = WebDriverWait(browser ,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="grille"]/table/tr[1]'))).text
      word_to_find = word_to_find.replace(" ","")
      size_file = len(word_to_find)
      print("taille du mot : ", size_file)

      words = initiatilisationTabs(words,letters,size_file,firstLetter_file)
      #word_to_find = find_word(words,line)
      #tant que le mot n'est pas trouvé, on continue
      found = False
      countTurn = 0
      while not(found):
            print("Nombre de mot restant",len(words))
            if len(words) == 0:
                  print("[ERREUR] Il n'y a plus de mot")
                  break
            #si le mot senatrice n'est plus dans la liste
            #if not(find_word(words,debug)):
                  #print("[ERREUR] Le mot n'est plus dans la liste")
                  #break
            countTurn += 1
            print("Tour n°",countTurn)
            best_word_found = best_word(words)
            #best_word_found = random_word(words)
            print("Meilleur mot : ",best_word_found.word)
            #ecrit le mot dans le browser
            ecritMot(browser,best_word_found,letters)
            #mask = getMask(best_word_found,word_to_find)
            mask = getMaskWeb(browser,size_file,countTurn)
            print("Masque : ",mask)
            if checkMask(mask) == True:
                  print("Mot trouvé !")
                  found = True
                  return countTurn
            else:
                  #filtre words
                  filter_words(words,mask,best_word_found)
                  #supprime le best word
                  #delete_word(words,best_word_found)
      print("Nombre de tour : ",countTurn)
      browser.close()

def main():
      #ouvre le navigateur
      browser = webdriver.Chrome()
      browser.get(url)
      browser.find_element(By.XPATH,'//*[@id="panel-fenetre-bouton-fermeture"]').click()
      nbTry = 100
      count = 0
      min = 100
      max = 0
      countWin = 0
      countLose =   0
      counts = [0 * i for i in range(1,21)]
      for i in range(nbTry):
            print("Tour n°",i+1)
            res = game(browser)
            count += res
            counts[res] += 1
            if res <= 6:
                  countWin += 1
            else:
                  countLose += 1
            if res < min:
                        min = res
            if res > max:
                  max = res
      print("Moyenne de tour : ",count/nbTry)
      print("Minimum de tour : ",min)
      print("Maximum de tour : ",max)
      print("Nombre de victoire : ",countWin)
      print("Nombre de défaite : ",countLose)
      for i in range(len(counts)):
            if counts[i] != 0:
                  print("Nombre de tour de ",i," : ",counts[i])

if __name__=="__main__":
      main()

