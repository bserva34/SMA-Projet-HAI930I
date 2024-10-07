import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import random
import json

def charger_blagues(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return json.load(f)['blagues']

# Charger les blagues depuis le fichier JSON
blagues = charger_blagues('blagues.json')

# Liste des blagues déjà racontées (initialement vide)
blagues_racontees = []


# Chargement des mots et des traductions depuis un fichier JSON
def charger_mots_traduction(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return json.load(f)

# Charger les mots depuis le fichier JSON
mots_traduction = charger_mots_traduction('mots_traduction.json')

# Liste des mots disponibles (initialement tous les mots)
mots_disponibles = list(mots_traduction.keys())

# Fonction pour charger les phrases à trous depuis un fichier JSON
def charger_phrases_trous(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return json.load(f)['phrases']

# Charger les phrases depuis le fichier JSON
phrases_a_trous = charger_phrases_trous('phrases_a_trous.json')

def charger_phrases_construction(fichier):
    with open(fichier, 'r', encoding='utf-8') as f:
        return json.load(f)['phrases']

# Charger les phrases de construction depuis le fichier JSON
phrases_construction = charger_phrases_construction('phrases_construction.json')


# Variables pour compter les mots appris et le compteur d'histoires
compteur_appris = 0
compteur_histoire = 0

# Fonction pour mettre à jour la fenêtre principale
def mettre_a_jour_fenetre_principale():
    global compteur_histoire, compteur_appris
    compteur_label.config(text=str(compteur_appris))

    # Vérification pour incrémenter le compteur_histoire chaque fois que compteur_appris dépasse une dizaine
    if compteur_appris > 0 and compteur_appris % 10 == 0:
        compteur_histoire += 1
        h_label.config(text=str(compteur_histoire))  # Mettre à jour l'affichage du compteur d'histoires

# Fonction pour afficher 3 mots aléatoires
def mode_free():
    global mots_disponibles, compteur_appris

    # Vérifier s'il reste au moins 3 mots
    if len(mots_disponibles) < 3:
        messagebox.showinfo("Mode Free", "Il ne reste pas assez de mots !")
        return

    # Choisir 3 mots aléatoires parmi les mots disponibles
    mots_choisis = random.sample(mots_disponibles, 3)

    # Création d'une nouvelle fenêtre pour afficher les mots
    free_window = tk.Toplevel(root)
    free_window.title("Choisis un mot à traduire")
    free_window.geometry("400x300")
    free_window.config(bg="#ff6888")

    # Variable pour afficher la traduction
    traduction_label = tk.Label(free_window, text="", font=("Arial", 14), bg="#ff6888")
    traduction_label.pack(pady=20)

    # Bouton "Suivant" masqué au départ
    suivant_button = tk.Button(free_window, text="Suivant", font=("Arial", 14), command=lambda: suivant(free_window))
    suivant_button.pack(pady=20)
    suivant_button.pack_forget()  # Masquer le bouton initialement

    def afficher_traduction(mot):
        global compteur_appris

        traduction = mots_traduction[mot]
        traduction_label.config(text=f"La traduction de '{mot}' est '{traduction}'")

        # Retirer le mot de la liste des mots disponibles
        mots_traduits.append(mot)
        mots_disponibles.remove(mot)

        # Incrémenter le compteur et mettre à jour l'affichage
        compteur_appris += 1
        mettre_a_jour_fenetre_principale()

        # Désactiver les boutons pour empêcher une nouvelle sélection
        for btn in buttons:
            btn.config(state=tk.DISABLED)

        # Afficher le bouton "Suivant"
        suivant_button.pack(pady=20)

    # Liste pour stocker les boutons (afin de les désactiver après la sélection)
    buttons = []

    # Affichage des boutons pour chaque mot
    for mot in mots_choisis:
        btn_mot = tk.Button(free_window, text=mot, font=("Arial", 14), command=lambda m=mot: afficher_traduction(m))
        btn_mot.pack(pady=10)
        buttons.append(btn_mot)

    # Fonction pour passer à une nouvelle série de mots
    def suivant(window):
        window.destroy()  # Fermer la fenêtre actuelle
        mettre_a_jour_fenetre_principale()  # Mettre à jour la fenêtre principale
        mode_free()  # Charger une nouvelle fenêtre avec de nouveaux mots

# Fonction pour le mode Exercice
# Fonction pour le mode Exercice avec une fenêtre similaire à "Free"
# Fonction pour le mode Exercice avec feedback visuel
def mode_exercice():
    # Créer un sous-menu avec deux boutons pour "Traduction" et "Fill the hole"
    exercice_menu = tk.Toplevel(root)
    exercice_menu.title("Mode Exercice")
    exercice_menu.geometry("400x300")
    exercice_menu.config(bg="#ff6888")

    traduction_button = tk.Button(exercice_menu, text="Traduction", font=("Arial", 16), command=mode_exercice_traduction)
    traduction_button.pack(pady=20)

    fill_hole_button = tk.Button(exercice_menu, text="Fill the hole", font=("Arial", 16), command=mode_fill_the_hole)
    fill_hole_button.pack(pady=20)

    sentence_button = tk.Button(exercice_menu, text="Sentence Construction", font=("Arial", 16), command=mode_sentence_construction)
    sentence_button.pack(pady=20)


# Renommer la fonction existante en mode_exercice_traduction
def mode_exercice_traduction():
    global compteur_appris, mots_traduits, mots_disponibles

    if len(mots_traduits) == 0:
        messagebox.showinfo("Mode Exercice", "Il n'y a pas encore de mots appris !")
        return

    exercice_window = tk.Toplevel(root)
    exercice_window.title("Mode Traduction")
    exercice_window.geometry("400x300")
    exercice_window.config(bg="#ff6888")

    mot = random.choice(mots_traduits)
    exercice_label = tk.Label(exercice_window, text=f"Quelle est la traduction de '{mot}' ?", font=("Arial", 14), bg="#ff6888")
    exercice_label.pack(pady=20)

    traduction_entry = tk.Entry(exercice_window, font=("Arial", 14))
    traduction_entry.pack(pady=10)

    resultat_label = tk.Label(exercice_window, text="", font=("Arial", 14), bg="#ff6888")
    resultat_label.pack(pady=10)

    # Désactiver le bouton "Valider" si la réponse est correcte
    def verifier_traduction():
        global compteur_appris, mots_traduits, mots_disponibles
        nonlocal mot
        traduction_utilisateur = traduction_entry.get()

        if traduction_utilisateur.lower() == mots_traduction[mot].lower():
            resultat_label.config(text="Bonne réponse !", fg="green")
            compteur_appris+=2
            mettre_a_jour_fenetre_principale()
            mots_traduits.remove(mot)
            
            # Désactiver le bouton "Valider"
            valider_button.config(state=tk.DISABLED)
            mettre_a_jour_fenetre_principale()
            if mot in mots_disponibles:
                mots_disponibles.remove(mot)

            
        else:
            resultat_label.config(text=f"Mauvaise réponse. La traduction correcte est '{mots_traduction[mot]}'.", fg="red")

    # Passer à un nouveau mot
    def suivant():
        nonlocal mot
        if len(mots_traduits) == 0:
            messagebox.showinfo("Mode Exercice", "Tous les mots ont été traduits !")
            exercice_window.destroy()  # Fermer la fenêtre si plus de mots disponibles
            return

        mot = random.choice(mots_traduits)
        exercice_label.config(text=f"Quelle est la traduction de '{mot}' ?")
        traduction_entry.delete(0, tk.END)
        resultat_label.config(text="")
        valider_button.config(state=tk.NORMAL)  # Réactiver le bouton "Valider"

    # Bouton "Valider" pour vérifier la traduction
    valider_button = tk.Button(exercice_window, text="Valider", font=("Arial", 14), command=verifier_traduction)
    valider_button.pack(pady=10)

    # Bouton "Suivant" pour passer à un autre mot, même si la réponse est incorrecte
    suivant_button = tk.Button(exercice_window, text="Suivant", font=("Arial", 14), command=suivant)
    suivant_button.pack(pady=10)





def mode_fill_the_hole():
    fill_window = tk.Toplevel(root)
    fill_window.title("Mode Fill the hole")
    fill_window.geometry("600x400")
    fill_window.config(bg="#ff6888")

    # Sélectionner une phrase aléatoire parmi celles chargées depuis le fichier JSON
    phrase = random.choice(phrases_a_trous)

    # Affichage de la phrase et de l'indice
    phrase_label = tk.Label(fill_window, text=phrase["phrase"], font=("Arial", 14), bg="#ff6888")
    phrase_label.pack(pady=20)

    indice_label = tk.Label(fill_window, text=f"Indice: {phrase['indice']}", font=("Arial", 12), bg="#ff6888", fg="blue")
    indice_label.pack(pady=10)

    reponse_entry = tk.Entry(fill_window, font=("Arial", 14))
    reponse_entry.pack(pady=10)

    resultat_label = tk.Label(fill_window, text="", font=("Arial", 14), bg="#ff6888")
    resultat_label.pack(pady=10)

    explication_label = tk.Label(fill_window, text="", font=("Arial", 12), bg="#ff6888", fg="cyan")
    explication_label.pack(pady=10)

    def verifier_reponse():
        global compteur_appris
        reponse_utilisateur = reponse_entry.get()

        if reponse_utilisateur.lower() == phrase["reponse"].lower():
            resultat_label.config(text="Bonne réponse !", fg="green")
            compteur_appris+=3
            mettre_a_jour_fenetre_principale()
        else:
            resultat_label.config(text=f"Mauvaise réponse. La réponse correcte est '{phrase['reponse']}'.", fg="red")

        explication_label.config(text=f"Explication: {phrase['explication']}")

        # Remplacer le bouton "Valider" par "Suivant"
        valider_button.pack_forget()
        suivant_button.pack(pady=20)

    def suivant():
        # Choisir une nouvelle phrase et réinitialiser les éléments
        nonlocal phrase
        phrase = random.choice(phrases_a_trous)
        phrase_label.config(text=phrase["phrase"])
        indice_label.config(text=f"Indice: {phrase['indice']}")
        reponse_entry.delete(0, tk.END)
        resultat_label.config(text="")
        explication_label.config(text="")
        suivant_button.pack_forget()
        valider_button.pack(pady=20)

    valider_button = tk.Button(fill_window, text="Valider", font=("Arial", 14), command=verifier_reponse)
    valider_button.pack(pady=20)

    suivant_button = tk.Button(fill_window, text="Suivant", font=("Arial", 14), command=suivant)
    suivant_button.pack_forget()  # Masquer le bouton "Suivant" jusqu'à validation

def mode_sentence_construction():
    global phrases_construction

    # Vérifier s'il y a des phrases disponibles
    if len(phrases_construction) == 0:
        messagebox.showinfo("Mode Sentence Construction", "Aucune phrase disponible pour le moment.")
        return

    # Choisir une phrase aléatoire parmi celles disponibles
    phrase = random.choice(phrases_construction)

    # Créer une nouvelle fenêtre pour cet exercice
    sentence_window = tk.Toplevel(root)
    sentence_window.title("Sentence Construction")
    sentence_window.geometry("600x500")
    sentence_window.config(bg="#ff6888")

    # Afficher la phrase avec un trou
    phrase_label = tk.Label(sentence_window, text=phrase["phrase"], font=("Arial", 14), bg="#ff6888")
    phrase_label.pack(pady=20)

    # Label pour afficher l'explication après sélection
    explication_label = tk.Label(sentence_window, text="", font=("Arial", 12), bg="#ff6888", fg="blue")
    explication_label.pack(pady=20)

    # Fonction pour afficher l'explication en fonction du mot choisi
    def afficher_explication(option):
        explication = phrase["options"][option]
        explication_label.config(text=explication)

    # Création des boutons pour chaque option
    for option in phrase["options"]:
        option_button = tk.Button(sentence_window, text=option, font=("Arial", 14),
                                  command=lambda opt=option: afficher_explication(opt))
        option_button.pack(pady=5)

    # Bouton "Suivant" pour passer à une nouvelle phrase
    def suivant():
        sentence_window.destroy()  # Fermer la fenêtre actuelle
        mode_sentence_construction()  # Ouvrir une nouvelle phrase

    suivant_button = tk.Button(sentence_window, text="Suivant", font=("Arial", 14), command=suivant)
    suivant_button.pack(pady=20)





# Ajouter une nouvelle liste pour stocker les mots traduits
mots_traduits = []

# Fonction pour le mode History
# Fonction pour le mode History avec une fenêtre similaire à "Free"
def mode_history():
    global blagues, blagues_racontees, compteur_histoire

    # Vérifier si compteur_histoire est supérieur à 0
    if compteur_histoire <= 0:
        messagebox.showinfo("Mode History", "Pas assez de points d'histoire !")
        return

    # Créer une nouvelle fenêtre pour le mode History
    history_window = tk.Toplevel(root)
    history_window.title("Mode History")
    history_window.geometry("400x300")
    history_window.config(bg="#ff6888")

    # Vérifier s'il reste des blagues non racontées
    blagues_disponibles = [b for b in blagues if b not in blagues_racontees]
    if not blagues_disponibles:
        messagebox.showinfo("Mode History", "Toutes les blagues ont déjà été racontées !")
        history_window.destroy()
        return

    # Choisir une blague aléatoire parmi celles non racontées
    blague = random.choice(blagues_disponibles)

    # Label pour poser la question de la blague
    question_label = tk.Label(history_window, text=f"{blague['question']}", font=("Arial", 14), bg="#ff6888")
    question_label.pack(pady=20)

    # Bouton pour afficher la réponse
    def montrer_reponse():
        reponse_label = tk.Label(history_window, text=f" {blague['reponse']}", font=("Arial", 14), bg="#ff6888")
        reponse_label.pack(pady=20)

        # Ajouter la blague à la liste des blagues racontées
        blagues_racontees.append(blague)

        # Décrémenter compteur_histoire et mettre à jour l'affichage

        global compteur_histoire
        # Vérifier si compteur_histoire est supérieur à 0
        if compteur_histoire <= 0:
            messagebox.showinfo("Mode History", "Pas assez de points d'histoire !")
            return
        compteur_histoire -= 1
        h_label.config(text=str(compteur_histoire))

    # Bouton pour afficher la réponse
    reponse_button = tk.Button(history_window, text="Montrer la réponse", font=("Arial", 14), command=montrer_reponse)
    reponse_button.pack(pady=20)


# Création de la fenêtre principale
root = tk.Tk()
root.title("Apprentissage de l'anglais")
root.geometry("800x600")
root.config(bg="#ff6888")

# Ajout des boutons représentant les modes
button_free = tk.Button(root, text="LESSON", bg="cyan", font=("Arial", 16), command=mode_free)
button_free.place(x=150, y=250, width=150, height=150)

button_exercice = tk.Button(root, text="EXERCICE", bg="yellow", font=("Arial", 16), command=mode_exercice)
button_exercice.place(x=325, y=250, width=150, height=150)

button_history = tk.Button(root, text="JOKES", bg="red", font=("Arial", 16), command=mode_history)
button_history.place(x=500, y=250, width=150, height=150)

# Ajout de quelques éléments graphiques pour l'ambiance
bee_image = tk.PhotoImage(file="bee.png")
bee_label = tk.Label(root, image=bee_image, bg="#ff6888")
bee_label.place(x=0, y=50)

dino_image = tk.PhotoImage(file="dino.png")
dino_label = tk.Label(root, image=dino_image, bg="#ff6888")
dino_label.place(x=300, y=50)

astro_image = tk.PhotoImage(file="astro.png")
astro_label = tk.Label(root, image=astro_image, bg="#ff6888")
astro_label.place(x=680, y=50)

t_image = tk.PhotoImage(file="trois.png")
t_label = tk.Label(root, image=t_image, bg="#ff6888")
t_label.place(x=100, y=450)

etoile_image = tk.PhotoImage(file="etoile.png")
etoile_label = tk.Label(root, image=etoile_image, bg="#ff6888")
etoile_label.place(x=10, y=250)

# Initialiser le texte de l'étoile à 0
compteur_label = tk.Label(root, text=str(compteur_appris), font=("Arial", 20), fg="white", bg="#f5e935")
compteur_label.place(x=75, y=305)

book_image = tk.PhotoImage(file="book.png")
book_label = tk.Label(root, image=book_image, bg="#ff6888")
book_label.place(x=650, y=250)

h_label = tk.Label(root, text=str(compteur_histoire), font=("Arial", 20), fg="black", bg="#e86d4c")
h_label.place(x=730, y=330)

# Lancement de l'interface
root.mainloop()
