import os

# === Demander les informations ===
def prendre_commande(utilisateur_actuel):
    try:
        with open("reponses_barttd.txt", "a", encoding="utf-8") as fichier:
            while True:
                commande = input("Que voulez-vous ? (entrer un point '.' quand vous avez fini) ")

                if commande.lower() == ".":
                    break

                # === Formatage de la réponse ===
                reponse_formatee = f"Bar TDD, {utilisateur_actuel} : {commande}\n"

                # === Sauvegarde immédiate dans le fichier ===
                fichier.write(reponse_formatee)

        # === Fin de la boucle ===
        print("\n✓ Vos réponses ont été enregistrées dans 'reponses_barttd.txt'.")
        print("📁 Emplacement :", os.path.abspath("reponses_barttd.txt"))

    except Exception as e:
        print("\n❌ Une erreur est survenue :", e)
