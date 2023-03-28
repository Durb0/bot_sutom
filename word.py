import letter
import main
import json

class Word():
    def __init__(self,string:str):
        self.word:str = string
        self.percent:float = 0

    def calculatePercent(self,letters:list):
        self.percent = 0
        for i in range(len(self.word)):
                    self.percent += main.findLetter(letters,self.word[i]).getPercent(i)
        self.percent = self.percent/len(self.word)
        return self

    def getPercent(self):
        return self.percent

    def setPercent(self,percent:float):
        self.percent = percent
        return self

    def getWord(self):
        return self.word

    def getLetter(self,pos:int):
        return self.word[pos]

    def getSize(self):
        return len(self.word)
    
    #function who check if letter is in word
    def checkLetter(self,c:str) -> int:
        for i in range(self.getSize()):
            if self.getLetter(i) == c:
                return i
        return -1

    #function who print the word in json format
    def print_word(self):
        print(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    def calculatePercent(self,letters:list):
        self.percent = 0
        for i in range(len(self.word)):
            self.percent += main.findLetter(letters,self.word[i]).getPositionPercent(i)
        self.percent = self.percent/len(self.word)
        return self