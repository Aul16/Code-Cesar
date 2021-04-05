import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import ScrolledText
import re

try:
    from unidecode import unidecode
except ImportError:
    showerror(title="ERREUR", message="Veillez installer la librairie unidecode avec la commande : 'pip install "
                                      "unidecode'")
    sys.exit(0)


# Verifie l'existance des fichiers nécessaires
if not os.path.exists("dico.txt"):
    showerror(title="ERREUR", message="Dictionnaire manquant")
    sys.exit(0)
if not os.path.exists("logo.ico"):
    showerror(title="ERREUR", message="Logo manquant")
    sys.exit(0)

# valeurs
grey = "#282820"
light_grey = "#878787"

regex = re.compile(r'[\n]')


# Fonction pour chiffrer
def chiffrer():
    code_entry.delete(1.0, END)
    texte_initial = unidecode(texte_entry.get(1.0, END)[:-1])
    cle = int(key_entry_text.get())
    texte_chiffre = ""
    for compteur in range(0, len(texte_initial)):
        ascii_lettre = ord(texte_initial[compteur].upper())
        if ascii_lettre < 65 or ascii_lettre > 90:
            texte_chiffre += texte_initial[compteur]
            continue
        ascii_lettre_chiffree = ord(texte_initial[compteur].upper()) + cle
        while ascii_lettre_chiffree > 90:
            ascii_lettre_chiffree -= 26
        texte_chiffre += chr(ascii_lettre_chiffree)
    code_entry.insert(1.0, texte_chiffre)


# Fonction pour déchiffrer
def bouton_dechiffrer():
    texte_entry.delete(1.0, END)
    texte_initial = unidecode(code_entry.get(1.0, END)[:-1])
    cle = int(key_entry_text.get())
    texte_dechiffre = ""
    for compteur in range(0, len(texte_initial)):
        ascii_lettre = ord(texte_initial[compteur].upper())
        if ascii_lettre < 65 or ascii_lettre > 90:
            texte_dechiffre += texte_initial[compteur]
            continue
        ascii_lettre_dechiffree = ord(texte_initial[compteur].upper()) - cle
        while ascii_lettre_dechiffree < 65:
            ascii_lettre_dechiffree += 26
        texte_dechiffre += chr(ascii_lettre_dechiffree)
    texte_entry.insert(1.0, texte_dechiffre)


# Fonction pour déchiffrer dans le cassage de code
def casser_chiffrement(word, cle):
    texte_dechiffre = ""
    for compteur in range(0, len(word)):
        ascii_lettre = ord(word[compteur].upper())
        if ascii_lettre < 65 or ascii_lettre > 90:
            word += word[compteur]
            continue
        ascii_lettre_dechiffree = ord(word[compteur]) - cle
        while ascii_lettre_dechiffree < 65:
            ascii_lettre_dechiffree += 26
        texte_dechiffre += chr(ascii_lettre_dechiffree)
    return texte_dechiffre


# Force à entrer une clé valide
def key_validation(text):
    try:
        key = int(text)
        if len(text) > 3:
            return False
    except ValueError:
        if text == "":
            return True
        else:
            return False
    else:
        return True


def break_code():
    code = unidecode(code_entry.get(1.0, END))
    code = code.upper()
    code = code.split(" ")
    result = []
    with open("dico.txt", "r+") as dico:
        word_list = dico.readlines()
        for word in word_list:
            word = regex.sub("", word)
            word = unidecode(word)
            word = word.upper()
            for word_code in code:
                word_code = regex.sub("", word_code)
                for cle in range(0, 26):
                    word_decode = casser_chiffrement(word_code, cle)
                    if word_decode == word:
                        result.append(cle)
        texte_entry.delete(1.0, END)
        if not result == []:
            result = dict([(n, result.count(n)) for n in set(result)])
            returned_string = ""
            total = 0
            for total_correspond in result.values():
                total += total_correspond
            for cle, nbr in result.items():
                returned_string += "clé {} : {}% \n".format(cle, round((nbr/total) * 100), 1)
            texte_entry.insert(1.0, "Clé(s) possible(s) : \n{}".format(returned_string))
        else:
            texte_entry.insert(1.0, "Aucune clé trouvée")
        dico.close()


if __name__ == '__main__':

    # Creer une fenêtre
    window = Tk()

    # Paramètres de la fenêtre
    window.title("Code César")
    window.geometry("480x360")
    window.minsize(480, 400)
    window.iconbitmap("logo.ico")
    window.config(bg=grey)

    # Creer une frame
    frame = Frame(window, bg=grey)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)

    keyValidationCommand = frame.register(key_validation)

    # Composants
    # Gauche
    label_title = Label(frame, text="CODE CESAR", bg=grey, fg=light_grey, font=("Segoe Print", 50))
    label_title.grid(row=0, column=0, columnspan=2, padx=5, sticky="ew")

    label_texte = Label(frame, text="Texte déchiffré : ", font=("Segoe Print", 10), bg=grey, fg=light_grey)
    label_texte.grid(row=1, column=0, sticky="sew", padx=5)

    """texte_entry_text = StringVar()
    texte_entry = Entry(frame, font=("Segoe Print", 10), bg=grey, fg=light_grey, insertbackground=light_grey,
                        exportselection=0, textvariable=texte_entry_text)
    texte_entry.grid(row=2, column=0, sticky="nsew", padx=5, pady=(0, 5))"""

    texte_entry = ScrolledText(master=frame, wrap=WORD, bg=grey, fg=light_grey, insertbackground=light_grey)
    texte_entry.grid(row=2, column=0, sticky="nswe", padx=5, pady=(0, 5))

    label_key = Label(frame, text="Clé : ", font=("Segoe Print", 10), bg=grey, fg=light_grey)
    label_key.grid(row=3, column=0, sticky="nse", padx=2, pady=(0, 5))

    boutton_chiffrer = Button(frame, text="CHIFFRER", font=("Segoe Print", 10), bg=light_grey, fg=grey,
                              command=chiffrer)
    boutton_chiffrer.grid(row=4, column=0, padx=5, sticky="ew", pady=(0, 5))

    boutton_quitter = Button(frame, text="QUITTER", font=("Segoe Print", 10), bg=light_grey, fg=grey,
                             command=window.quit)
    boutton_quitter.grid(row=5, column=0, padx=5, sticky="ew")

    # Droite
    label_chiffre = Label(frame, text="Texte chiffré : ", font=("Segoe Print", 10), bg=grey, fg=light_grey)
    label_chiffre.grid(row=1, column=1, sticky="ew", padx=5)

    """
    code_entry_text = StringVar()
    code_entry = Entry(frame, font=("Segoe Print", 10), bg=grey, fg=light_grey, insertbackground=light_grey,
                       exportselection=0, textvariable=code_entry_text)
    code_entry.grid(row=2, column=1, sticky="nsew", padx=5, pady=(0, 5))"""

    code_entry = ScrolledText(master=frame, wrap=WORD, bg=grey, fg=light_grey, insertbackground=light_grey)
    code_entry.grid(row=2, column=1, sticky="nsew", padx=5, pady=(0, 5))

    key_entry_text = StringVar()
    key_entry = Entry(frame, font=("Segoe Print", 10), bg=grey, fg=light_grey, justify="center",
                      insertbackground=light_grey, validate="all", validatecommand=(keyValidationCommand, "%P"),
                      exportselection=0, textvariable=key_entry_text)
    key_entry.grid(row=3, column=1, sticky="nsw", pady=(0, 5), padx=2)

    boutton_dechiffrer = Button(frame, text="DECHIFFRER", font=("Segoe Print", 10), bg=light_grey, fg=grey,
                                command=bouton_dechiffrer)
    boutton_dechiffrer.grid(row=4, column=1, padx=5, sticky="ew", pady=(0, 5))

    boutton_casser_un_code = Button(frame, text="CASSER UN CODE", font=("Segoe Print", 10), bg=light_grey, fg=grey,
                                    command=break_code)
    boutton_casser_un_code.grid(row=5, column=1, padx=5, sticky="ew")

    # Afficher la frame
    frame.pack(fill=BOTH, expand=YES)

    # Creer une barre de menu
    menu_bar = Menu(window)

    # Creer un menu
    menu = Menu(menu_bar, tearoff=0)
    menu.add_command(label="Chiffrer", command=chiffrer)
    menu.add_command(label="Déchiffrer", command=bouton_dechiffrer)
    menu.add_command(label="Casser un code", command=break_code)
    menu.add_command(label="Quitter", command=window.quit)

    menu_bar.add_cascade(label="Commandes", menu=menu)

    # Configurer la fenêtre
    window.config(menu=menu_bar)

    # Afficher la fenêtre
    window.mainloop()
