import json

class PositionData():
          def __init__(self):
                    self.count:int = 0
                    self.percent:float = 0
          
          def getCount(self):
                    return self.count

          def getPercent(self):
                    return self.percent

          def addCount(self):
                    self.count += 1
          
          def updatePercent(self,length):
                    self.percent = self.count/length

class Letter():
          def __init__(self,c:str):
                    self.c:str = c
                    self.count:int = 0
                    self.row = -1
                    self.column = -1
                    self.getCoordinates()
                    self.positions:list = [PositionData() for i in range(9)]
                    

          def add(self,pos:int):
                    self.count += 1
                    self.positions[pos].addCount()
                    self.positions[pos].updatePercent(self.count)
                    return self

          def getCount(self):
                    return self.count

          def getLetter(self):
                    return self.c
          
          #ajoute 1 a chaque pourcent position
          def addPositionsPercent(self):
                    for i in range(9):
                              self.positions[i].percent += 1
                    return self

          #retourne vrai si la lettre est une voyelle
          def isVowel(self):
                    if self.c == "A" or self.c == "E" or self.c == "I" or self.c == "O" or self.c == "U" or self.c == "Y":
                              return True
                    else:
                              return False


          def getPositionCount(self,pos:int):
                    return self.positions[pos].getCount()

          def getPositionPercent(self,pos:int):
                    return self.positions[pos].getPercent()

          def isLetter(self,c:str):
                    if self.c == c:
                              return True
                    else:
                              return False

          #fonction qui affiche une lettre en format json
          def print_letter(self):
                    print(json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4))


         #get coordinates of the letter on keyboard
          def getCoordinates(self):
                    #row
                    if((self.getLetter()=='A')|(self.getLetter()=='Z')|(self.getLetter()=='E')|(self.getLetter()=='R')|(self.getLetter()=='T')|(self.getLetter()=='Y')|(self.getLetter()=='U')|(self.getLetter()=='I')|(self.getLetter()=='O')|(self.getLetter()=='P')):
                              self.row= 1
                    elif((self.getLetter()=='Q')|(self.getLetter()=='S')|(self.getLetter()=='D')|(self.getLetter()=='F')|(self.getLetter()=='G')|(self.getLetter()=='H')|(self.getLetter()=='J')|(self.getLetter()=='K')|(self.getLetter()=='L')|(self.getLetter()=='M')):
                              self.row= 2
                    else:
                              self.row= 3
                    #column
                    if((self.getLetter()=='A')|(self.getLetter()=='Q')):
                              self.column= 1
                    if((self.getLetter()=='Z')|(self.getLetter()=='S')|(self.getLetter()=='W')):
                              self.column= 2
                    if((self.getLetter()=='E')|(self.getLetter()=='D')|(self.getLetter()=='X')):
                              self.column= 3
                    if((self.getLetter()=='R')|(self.getLetter()=='F')|(self.getLetter()=='C')):
                              self.column= 4
                    if((self.getLetter()=='T')|(self.getLetter()=='G')|(self.getLetter()=='V')):
                              self.column= 5
                    if((self.getLetter()=='Y')|(self.getLetter()=='H')|(self.getLetter()=='B')):
                              self.column= 6
                    if((self.getLetter()=='U')|(self.getLetter()=='J')|(self.getLetter()=='N')):
                              self.column= 7
                    if((self.getLetter()=='I')|(self.getLetter()=='K')):
                              self.column= 8
                    if((self.getLetter()=='O')|(self.getLetter()=='L')):
                              self.column= 9
                    if((self.getLetter()=='P')|(self.getLetter()=='M')):
                              self.column= 10