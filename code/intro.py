import questionary
import os
import sys
import subprocess
from pathlib import Path




RESPONSE_FILE = Path("runner.txt")




def open_with_default_app(path: Path):
    """Ouvre un fichier avec l'application par défaut selon le système d'exploitation."""
    if not path.exists():
        path.write_text(" Fichier créé automatiquement.\n")
    if sys.platform.startswith("win"):
        os.startfile(str(path))
    elif sys.platform == "darwin":  # macOS
        subprocess.run(["open", str(path)])
    else:  # Linux
        subprocess.run(["xdg-open", str(path)])

mdp_utilisateurs = {
    "king":"Thomas",
    "21": "Roberto M.",
    "22": "JEAN-PHILIPPE C",
    "26": "ZACHARY G.",
    "28": "DAPHNE P",
    "33": "TOUPIN CHARLIE",
    "42": "meunier michael",
    "44": "MATHILDE V.",
    "45": "jeremie leblanc",
    "65": "megann d",
    "88": "JP RONALDI",
    "93": "ANGI",
    "97": "marie laurence",
    "98": "alyson trottier",
    "102": "ELOISE G",
    "127": "ELOI B",
    "136": "ALEXANNE M",
    "295": "VICKY",
    "796": "Mario Antonio",
    "797": "Mya M-D",
    "798": "Benjamin C.",
    "799": "LOUKA B.",
    "800": "EVE G.",
    "801": "Jasmine Roof",
    "802": "Aurore N.",
    "803": "Olivier B.",
    "804": "STEPHANIA",
    "805": "DAMIEN BG",
    "806": "Florence De C.",
    "807": "Eli B.",
    "808": "marie lou r",
    "810": "ROBERTO M",
    "811": "JACOB D",
    "815": "SHANIE S",
    "820": "MONGRAIN MYA",
    "823": "FERRON DAVID",
    "828": "Jasmine R",
    "829": "Élodie G",
    "835": "Juliette DB",
    "839": "Franck T",
    "840": "Max-Antoine D",
    "841": "Emerick S.",
    "843": "Pascale B.",
    "847": "Allison S",
    "850": "Madyson V.",
    "851": "Émile T.",
    "852": "Laurence R.",
    "853": "Marie-Joelle R.",
    "854": "Joanie B.",
    "855": "Mégane B.",
    "856": "Juliette B.",
    "858": "Marianne M.",
    "861": "Élie SY",
    "863": "Sandrine N.",
    "869": "Maryane B.",
    "871": "Corina L.",
    "872": "Anthony R.",
    "873": "Marie-Lune S.",
    "878": "Mélissa H.",
    "880": "Isabelle C.",
    "882": "Rose B.",
    "883": "Alexann M.",
    "888": "Lauralie H.",
    "890": "Sharlee M.",
    "891": "Josiane B.",
    "892": "Martine R.",
    "893": "Aurélie C",
    "898": "Maggie Lajoie",
    "8742": "Invité"
    

    
}



while True:
    mdp = input("entrer votre mot de passe").strip().lower()
    if mdp in mdp_utilisateurs:
        print(f"Bienvenue {mdp_utilisateurs[mdp]}!")
        utilisateur_actuel = mdp_utilisateurs[mdp]
        break
    elif mdp == "2733":
        print("accès au runner")
        open_with_default_app(RESPONSE_FILE)
             
    else:
        print("Votre mot de passe est incorrect")

choix = questionary.select(
 "Où voulez-vous recevoir votre commande?",
    choices=[
    "Bar simply",
    "Bar TDD" ,
    "Loges",
    "Nord",
    "Poutinerie",
    "Principale",
    "Sud",
    "Zone TDD",
    "Rackeur",
    "Quitter"  
   ]
   ).ask()
if choix == "Bar simply":
    print("Vous êtes maintenant au bar symply")
    import barsimpl
    barsimpl.prendre_commande(utilisateur_actuel)
elif choix == "Bar TDD":
    print("Vous êtes maintenant au bar TDD")
    import bartdd
    bartdd.prendre_commande(utilisateur_actuel)
elif choix == "Loges":
    print("Vous êtes maintenant aux loges")
    import loge
    loge.prendre_commande(utilisateur_actuel)
elif choix == "Nord":
    print("Vous êtes maintenant à  la nord")
    import nord
    nord.prendre_commande(utilisateur_actuel)
elif choix == "Poutinerie":
    print("Vous êtes maintenant à  la poutinerie")
    import pout
    pout.prendre_commande(utilisateur_actuel)
elif choix == "Rackeur":
    print("Vous êtes maintenant aux rackeurs")
    import racker
    racker.prendre_commande(utilisateur_actuel)
elif choix == "Principale":
    print("Vous êtes maintenant à  la principale")
    import princip  
    princip.prendre_commande(utilisateur_actuel)
elif choix == "Sud":
    print("Vous êtes maintenant à  la sud")
    import sud
    sud.prendre_commande(utilisateur_actuel)
elif choix == "Zone TDD":
    print("Vous êtes maintenant à  la zone TDD")
    import zonetdd
    zonetdd.prendre_commande(utilisateur_actuel)
elif choix == "Quitter":
    sys.exit()

