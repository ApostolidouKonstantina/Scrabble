import random
import itertools

class Sakclass():
    letters=["","Α","Β","Γ","Δ","Ε","Ζ","Η","Θ","Ι","Κ","Λ","Μ","Ν","Ξ","Ο","Π","Ρ","Σ","Τ","Υ","Φ","Χ","Ψ","Ω"]
    
    def __init__(self):
        self.remainingletters=104
        self.letdic =dict()

    def randomize_sak(self):
        self.letdic={"":[0,2],"Α":[1,12],"Β":[8,1], "Γ":[4,2], "Δ":[4,2], "Ε":[1,8], "Ζ":[10,1], "Η":[1,7], 
        "Θ":[10,1], "Ι":[1,8], "Κ":[2,4], "Λ":[3,3], "Μ":[3,3], "Ν":[1,6], "Ξ":[10,1], "Ο":[1,9], "Π":[2,4],
        "Ρ":[2,5], "Σ":[1,7], "Τ":[1,8], "Υ":[2,4], "Φ":[8,1], "Χ":[8,1], "Ψ":[10,1], "Ω":[3,3]}
        return 

    def getletters(self,num):
        if (self.remainingletters < num):
            return "n-letters"
        newletters=list()
        for i in range(0,num):
            letter = "-1"
            while (letter=="-1"):
                r = random.randint(0, 24)
                if (self.letdic[Sakclass.letters[r]][1]>0):
                    letter=Sakclass.letters[r]
                    points=self.letdic[Sakclass.letters[r]][0]
                    self.letdic[Sakclass.letters[r]][1]-=1
                    self.remainingletters-=1
            newletters.append([letter,points])
        return newletters


    def putbackletters(self,oldletters):
        for i in range (0,7):
            self.letdic[oldletters[i][0]][1]+=1
        self.remainingletters+=7
        newletters=self.getletters(7)
        return newletters
    
    def __repr__(self):
        return f'Στο σακουλάκι παραμένουν: {self.remainingletters} γράμματα\n'



class Player:
    def __init__(self,name,s):
        self.mypoints=0
        self.name=name
        self.myletters=s.getletters(7)

    def __repr__(self):
        return f'Παίκτης: {self.name}     Score: {self.mypoints} \nΓράμματα: {self.myletters}\n'

class Human(Player):
    def play(self, word, s, g):
        if (g.exists(word)):
            ls=[*word]
            lt=list()
            for x in range(0,len(self.myletters)):
                lt.append([self.myletters[x][0],self.myletters[x][1],False]) #letter,points,used?
            mistakes=0
            pnts=0
            for i in range(0,len(ls)):
                letterexists = False
                for j in range (0,len(lt)):
                    if ((ls[i]==lt[j][0]) & (lt[j][2]==False)):
                        letterexists=True
                        lt[j][2]==True
                        pnts+=lt[j][1]
                        break
                if (not letterexists):
                    mistakes+=1
            
            if (mistakes==0): #all letters match
                self.mypoints+=pnts
                for x in ls: #new list, used removing letters
                    for ii in range(0,len(self.myletters)):
                        if (x==self.myletters[ii][0]):
                            self.myletters.remove(self.myletters[ii])
                            break
                newls=s.getletters(7-len(self.myletters))
                if (newls!="n-letters"):
                    for x in range(0,len(newls)):
                        self.myletters.append(newls[x])
                    return pnts, ""
                return pnts,"n-letters"
            
            bldr=0
            for i in range(0,len(self.myletters)):
                if (""==self.myletters[i][0]):
                    bldr+=1
            if (mistakes<=bldr): #letters match and there are enough plain ones to cover up
                self.mypoints+=pnts
                for x in ls: #new list, used removing letters
                    for ii in range(0,len(self.myletters)):
                        if (x==self.myletters[ii][0]):
                            self.myletters.remove(self.myletters[ii])
                            break
                        if ((mistakes>0) & (self.myletters[ii][0]=='')):
                            mistakes+=1
                            self.myletters.remove(self.myletters[ii])
                            break
                newls=s.getletters(7-len(self.myletters))
                if (newls!="n-letters"):
                    for x in range(0,len(newls)):
                        self.myletters.append(newls[x])
                    return pnts, ""
                return pnts,"n-letters"
            return "n-match" #letters weren't matched
        return "n-exists"
        
class Computer(Player):
    def play(self,alg,s,g):
        astring=self.myletters[0][0]
        for x in range(1,len(self.myletters)):
            astring += self.myletters[x][0]
        if (alg==1):
            result=self.minletters(astring,g)  
        elif (alg==2):
            result = self.maxletters(astring,g)  
        else:
            result = self.smart(astring,g)  
        if (result[1]==0):
            return result,"pass"
        ls=[*result[0]]
        for x in ls: #new list, used removing letters
            for ii in range(0,len(self.myletters)):
                if (x==self.myletters[ii][0]):
                    self.myletters.remove(self.myletters[ii])
                    break
        newls=s.getletters(7-len(self.myletters))
        if (newls!="n-letters"):
            for x in range(0,len(newls)):
                self.myletters.append(newls[x])
            return result, "ok"
        return result,"n-letters"

    
    def minletters(self,astring,g):
        for leng in range(2,8):
            alist = list(map("".join, itertools.permutations(astring,leng)))
            for x in range(0,len(alist)):
                if (g.exists(alist[x])):
                    pnts=0
                    ls=[*alist[x]]
                    for i in range(0,len(ls)):
                        for j in range (0,len(self.myletters)):
                            if (ls[i]==self.myletters[j][0]):
                                pnts+=self.myletters[j][1]
                    return alist[x],pnts
        return '',0 
    
    def maxletters(self,astring,g):
        for leng in range(7,1,-1):
            alist = list(map("".join, itertools.permutations(astring,leng)))
            for x in range(0,len(alist)):
                if (g.exists(alist[x])):
                    pnts=0
                    ls=[*alist[x]]
                    for i in range(0,len(ls)):
                        for j in range (0,len(self.myletters)):
                            if (ls[i]==self.myletters[j][0]):
                                pnts+=self.myletters[j][1]
                    return alist[x],pnts
        return '',0   
    
    def smart(self,astring,g):
        word=['',0]
        for leng in range(2,8):
            alist = list(map("".join, itertools.permutations(astring,leng)))
            for x in range(0,len(alist)):
                if (g.exists(alist[x])):
                    pnts=0
                    ls=[*alist[x]]
                    for i in range(0,len(ls)):
                        for j in range (0,len(self.myletters)):
                            if (ls[i]==self.myletters[j][0]):
                                pnts+=self.myletters[j][1]
                    if (pnts>word[1]):
                        word[0]=alist[x]
                        word[1]=pnts    
        return word[0],word[1] 
        
      
            
class Game():
    
    def __init__(self):
        self.moves=0
        awords = list()
        with open('greek7.txt','r', encoding='utf8') as let_file:
            Game.awords = let_file.read().splitlines()
    
    def setup(self,algrthm,name):     
        self.algrthm = algrthm
        sak=Sakclass()
        sak.randomize_sak()
        human=Human(name,sak)
        comp=Computer("Computer",sak)
        return sak,human,comp
        
    def run(self,play,player,sak,game):
        print(player)
        if (play==1):
            word=input("Λέξη: ")
            result = player.play(word,sak,game)
            while ((result=="n-match") or (result=="n-exists")): 
                if (word=="q"): #quit
                    return "quit"
                if (word=="p"): #pass
                    player.myletters=sak.putbackletters(player.myletters)
                    print(player)
                    print("\n------------------------------------------------------------------")
                    return ""   
                if (result=="n-match"):
                    word = input("\nΔεν έχεις όλα τα γράμματα για αυτή τη λέξη. Προσπάθησε ξανά: ")
                if (result=="n-exists"):
                    word = input("\nΗ λέξη δεν υπάρχει. Προσπάθησε ξανά: ")  
                result = player.play(word,sak,game)   
            print("Πόντοι λέξης: ", result[0], "\n")   
            self.moves+=1
            if (result[1]=="n-letters"):
                print("\n------------------------------------------------------------------")
                return "n-letters"
            print(player)
            print(sak)
            input("\nΠάτα Enter για συνέχεια ")    
            print("\n------------------------------------------------------------------")
            
        else:
            result=player.play(self.algrthm,sak,game)
            if (result[1]=="pass"): 
                player.myletters=sak.putbackletters(player.myletters)
                print(player)
                print("\n------------------------------------------------------------------")
                return ""  
            print("Λέξη: ", result[0][0])
            player.mypoints+=result[0][1]
            print("Πόντοι λέξης: ", result[0][1], "\n")
            self.moves+=1
            if (result[1]=="n-letters"):
                print("\n------------------------------------------------------------------")
                return "n-letters"
            print(player)
            print(sak)
            input("\nΠάτα Enter για συνέχεια ")   
            print("\n------------------------------------------------------------------")
            
        return ""

    def end(self,human,comp,status):
        print(f"\nΤελικό score:  {human.name} - {human.mypoints}  vs Computer - {comp.mypoints}\n")
        if (status=="quit"):
            print("Νικητής Computer, λόγω παραίτησης παίκτη")
            with open ("history_file.txt","a",encoding='utf8') as f:
                f.write(f"--Νικητής: Computer  -Score (Computer, {human.name}): {comp.mypoints} vs {human.mypoints}  -Κινήσεις: {self.moves}   -Λόγος λήξης: Παραίτηση {human.name}\n")
        else:
            if (human.mypoints>comp.mypoints):
                print("*** Νίκη ***")
                with open ("history_file.txt","a",encoding='utf8') as f:
                    f.write(f"--Νικητής: {human.name}  -Score (Computer, {human.name}): {comp.mypoints} vs {human.mypoints}  -Κινήσεις: {self.moves}  -Λόγος λήξης: Μη επαρκή γράμματα\n")
            elif (human.mypoints==comp.mypoints):
                print("*** Ισοπαλία ***")
                with open ("history_file.txt","a",encoding='utf8') as f:
                    f.write(f"--Ισοπαλία  -Score (Computer, {human.name}): {comp.mypoints} vs {human.mypoints}  -Κινήσεις: {self.moves}  -Λόγος λήξης: Μη επαρκή γράμματα\n")
            else:
                print("*** Ήττα ***")
            with open ("history_file.txt","a",encoding='utf8') as f:
                f.write(f"--Νικητής: Computer  -Score (Computer, {human.name}): {comp.mypoints} vs {human.mypoints}  -Κινήσεις: {self.moves}  -Λόγος λήξης: Μη επαρκή γράμματα\n")
    
    def exists(self,word):
        first = 0
        last = len(self.awords)-1
        while ((first<=last)):
            pos = 0
            mid = (first + last)//2
            if (self.awords[mid] == word):
                pos = mid
                return True
            else:
                if (word < self.awords[mid]):
                    last = mid-1
                else:
                    first = mid+1
        return False
    
    def __repr__(self):
        return f''