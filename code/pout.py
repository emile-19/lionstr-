import os

# === Demander les informations ===
def prendre_commande(utilisateur_actuel):
    try:
        with open("reponses.txt", "a", encoding="utf-8") as fichier:
            while True:
                zonetd = input("Que voulez-vous ? (entrer un point quand vous avez fini) ")

                if zonetd.lower() == ".":
                    break

                # === Formatage de la réponse ===
                reponse_formatee = f"Poutinerie, {utilisateur_actuel} : {zonetd}\n"

                # === Sauvegarde immédiate dans le fichier ===
                fichier.write(reponse_formatee)

        # === Fin de la boucle ===
        print("\n✓ Vos réponses ont été enregistrées dans 'reponses.txt'.")
        print("📁 Emplacement :", os.path.abspath("reponses.txt"))

    except Exception as e:
        print("\n❌ Une erreur est survenue :", e)

