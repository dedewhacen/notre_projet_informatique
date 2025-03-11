# Définition des modules et des coefficients selon l'image
modules = {
    "UE11": {"GCGP_31": 3, "GCGP_32": 2, "GCGP_33": 2},
    "UE12": {"GCGP_34": 3, "GCGP_35": 3, "GCGP_36": 2},  # GCGP_35 doit être estimé
    "UE13": {"GCGP_37": 3, "GCGP_38": 1},  # GCGP_38 doit être estimé
    "UE14": {"ST_31": 1},
    "UE15": {"HE_31": 4, "HE_32": 3, "HE_33": 1}
}

# Fonction pour calculer la moyenne générale
def calculer_moyenne():
    total_general = 0
    total_coeff_general = 0
    notes = {}  # Stocker les notes saisies

    for module, matieres in modules.items():
        print(f"\n=== Calcul de la moyenne du module : {module} ===")
        total = 0
        total_coeff = 0

        for matiere, coeff in matieres.items():
            if matiere in ["GCGP_35", "GCGP_38"]:
                print(f"Estimation de la note pour la matière {matiere} en fonction des autres matières du module...")
                matieres_existantes = {k: v for k, v in matieres.items() if k not in ["GCGP_35", "GCGP_38"]}
                note_estimee = sum(notes[k] * v for k, v in matieres_existantes.items()) / sum(matieres_existantes.values())
                print(f"Note estimée pour {matiere} = {note_estimee:.2f}")
                note = note_estimee
            else:
                while True:
                    try:
                        note = float(input(f"Entrez la note pour la matière {matiere} : "))
                        if 0 <= note <= 20:
                            break
                        else:
                            print("Veuillez entrer une note valide entre 0 et 20.")
                    except ValueError:
                        print("Veuillez entrer un nombre valide.")

            notes[matiere] = note
            total += note * coeff
            total_coeff += coeff

        moyenne_module = total / total_coeff
        total_general += total
        total_coeff_general += total_coeff

        print(f"Moyenne du module {module} : {moyenne_module:.2f}")

    moyenne_generale = total_general / total_coeff_general
    print(f"\n=== Moyenne générale de la maquette : {moyenne_generale:.2f} ===")

# Exécuter le programme
calculer_moyenne()