
def guidelines():
    '''Κλάσεις: Sakclass(), Player, Human(Player), Computer(Player), Game().
    Κληρονομικότητα εφαρμόστηκε στις κλάσεις Human και Computer, των οποίων ανώτερη αποτελεί η κλάση Player.
    Από αυτήν κληρονομούν τον κατασκευαστή __init__ (και το __repr__) και επομένως τις ιδιότητες name, mypoints, myletters.
    Οι λέξεις της γλώσσας οργανώνονται σε μια ordered λίστα (αφού είναι ήδη ταξινομημένα αλφαβητικά),
    και η προσπέλασή τους γίνεται μόνο από την μέθοδο exists της κλάσης Game με τη χρήση δυαδικής αναζήτησης, ώστε να μειωθεί σημαντικά ο χρόνος αναζήτησης.
    Ο υπολογιστής παίζει με τον αλγόριθμο1: min, max, smart. Από default παίζει με τον min,
    αλλά ο χρήστης μπορεί μέσω των 'ρυθμίσεων' στο αρχικό μενού επιλογής να επιλέξει όποια μέθοδο από τις 3 επιθυμεί.
    Κατά τη διάρκεια του παιχνιδιού, αν ο υπολογιστής δεν μπορεί να βρει πιθανή λέξη τότε πάει πάσο και αλλάζει γράμματα, δεν κάνει quit.
    Το quit του χρήστη είναι αμέσως ήττα του, ανεξάρτητα με το σκορ εκείνη τη στιγμή.
    Η καταγραφή του σκορ μετά την λήξη κάθε παιχνιδιού γίνεται σε αρχείο "history_file.txt".'''
    pass

import classes

algrthm=1
print("\n***SCRABBLE***\n\n1: Νέο Παιχνίδι\n2: Ρυθμίσεις\n3: Έξοδος")
choice=int(input("Η επιλογή σας: "))
while ((choice<1) & (choice>3)):
    choice=int(input("Λάθος επιλογή. Προσπαθήστε ξανά: "))

while (choice!=3):
    if (choice==2):
        print("\nΜέθοδοι Υπολογιστή: MINLETTERS (1), MAXLETTERS (2), SMART (3) \nΜε ποιόν από τους 3 θα θέλατε να παίζει;")
        algrthm = int(input("Πληκτρολογίστε 1, 2 ή 3: "))
        print("\nΗ αλλαγή αποθηκεύτηκε!")
    if (choice==1):
        game=classes.Game()
        n = input("\nΠληκτολόγισε το όνομά σου: ")
        sak,human,comp=game.setup(algrthm,n)
        
        print("------------------------------------------------------------------")
        status="running"
        while (status=="running"):
            result=game.run(1,human,sak,game)
            if ((result=="quit") or (result=="n-letters")):
                status=result                
            else:
                result=game.run(2,comp,sak,game)
                if (result=="n-letters"):
                    status=result
        
        game.end(human,comp,status)
        input("\nΠάτα Enter για συνέχεια ")   
    print("\n\n***SCRABBLE***\n\n1: Νέο Παιχνίδι\n2: Ρυθμίσεις\n3: Έξοδος")
    choice=int(input("Η επιλογή σας: "))
    
exit()    
    