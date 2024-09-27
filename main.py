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

# Variables pour compter les mots appris et le compteur d'histoires
compteur_appris = 0
compteur_histoire = 2

# Fonction pour mettre à jour la fenêtre principale
def mettre_a_jour_fenetre_principale():
    global compteur_histoire
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
def mode_exercice():
    global compteur_appris, mots_traduits

    # Vérifier s'il y a des mots déjà appris
    if len(mots_traduits) == 0:
        messagebox.showinfo("Mode Exercice", "Il n'y a pas encore de mots appris !")
        return

    # Choisir un mot déjà appris aléatoirement
    mot = random.choice(mots_traduits)

    # Demander à l'utilisateur la traduction du mot choisi
    traduction_utilisateur = tk.simpledialog.askstring("Exercice", f"Quelle est la traduction de '{mot}' ?")

    # Vérifier si la traduction est correcte
    if traduction_utilisateur and traduction_utilisateur.lower() == mots_traduction[mot].lower():
        messagebox.showinfo("Exercice", "Bonne réponse !")
        compteur_appris += 2  # Ajouter 2 au compteur
        mots_traduits.remove(mot)  # Retirer le mot de la liste
        mettre_a_jour_fenetre_principale()  # Mettre à jour la fenêtre principale
    else:
        messagebox.showinfo("Exercice", f"Mauvaise réponse. La traduction correcte est '{mots_traduction[mot]}'.")

# Ajouter une nouvelle liste pour stocker les mots traduits
mots_traduits = []

# Fonction pour le mode History
def mode_history():
    global blagues, blagues_racontees, compteur_histoire

    # Vérifier si compteur_histoire est supérieur à 0
    if compteur_histoire <= 0:
        messagebox.showinfo("Mode History", "Pas assez de points d'histoire !")
        return

    # Vérifier s'il reste des blagues non racontées
    blagues_disponibles = [b for b in blagues if b not in blagues_racontees]
    if not blagues_disponibles:
        messagebox.showinfo("Mode History", "Toutes les blagues ont déjà été racontées !")
        return

    # Choisir une blague aléatoire parmi celles non racontées
    blague = random.choice(blagues_disponibles)

    # Demander une confirmation pour écouter la blague
    confirmation = messagebox.askokcancel("Mode History", "Es-tu prêt pour une blague ?")
    
    if confirmation:
        # Raconter la blague
        messagebox.showinfo("Blague", f"{blague['question']}\n\nRéponse: {blague['reponse']}")

        # Ajouter la blague à la liste des blagues racontées
        blagues_racontees.append(blague)

        # Décrémenter compteur_histoire et mettre à jour l'affichage
        compteur_histoire -= 1
        h_label.config(text=str(compteur_histoire))

# Création de la fenêtre principale
root = tk.Tk()
root.title("Apprentissage de l'anglais")
root.geometry("800x600")
root.config(bg="#ff6888")

# Ajout des boutons représentant les modes
button_free = tk.Button(root, text="FREE", bg="cyan", font=("Arial", 16), command=mode_free)
button_free.place(x=150, y=250, width=150, height=150)

button_exercice = tk.Button(root, text="EXERCICE", bg="yellow", font=("Arial", 16), command=mode_exercice)
button_exercice.place(x=325, y=250, width=150, height=150)

button_history = tk.Button(root, text="HISTORY", bg="red", font=("Arial", 16), command=mode_history)
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
