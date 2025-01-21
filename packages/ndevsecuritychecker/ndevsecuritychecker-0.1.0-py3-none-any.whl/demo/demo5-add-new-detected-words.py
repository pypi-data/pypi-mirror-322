from src import dev_sec, sec_names


# Variable nécessaire a la fonction

path = "C:\\Users\\iguille\\base-project-structure\\tests\\testpath"
file_extension = [".py", ".yaml"]
file_extension2 = [".ts", ".txt"]

naming_convention = "camel_case"
naming_convention2 = "snake_case"
naming_convention3 = "uppercase"

print("Avant ajout variable custom\n")
dev_sec.print_result(
    dev_sec.retrieve_sensible_data(
            path, #Chemin a verifier (Obligatoire)
            file_extension,  #Extension des fichiers a verifier (Obligatoire)
            naming_convention2, #Convention de nommage des variables (Obligatoire)
            False, #Regarder directement si le nom du fichier est sensible ou non (Optionnel, Default: False)
            False, #Ajouter les fichiers sensibles au .gitignore (Optionnel, Default: False)
            False #Ajouter la sortie console dans un fichier texte (Optionnel, Default: False)
        )
    )

print("\n--------------------------------------------------\n")

# Ajouter des nouveau mots detecter
sec_names.add_new_sensible_var_name("test_new_var_name_snake_case", "snake_case")

# Fonction principale
# Trois premiers parametres obligatoires ! Le chemin a vérifier, les extensions des fichiers et la convention de nommage des variables
print("Apres ajout variable custom\n")
dev_sec.print_result(
    dev_sec.retrieve_sensible_data(
            path, #Chemin a verifier (Obligatoire)
            file_extension,  #Extension des fichiers a verifier (Obligatoire)
            naming_convention2, #Convention de nommage des variables (Obligatoire)
            False, #Regarder directement si le nom du fichier est sensible ou non (Optionnel, Default: False)
            False, #Ajouter les fichiers sensibles au .gitignore (Optionnel, Default: False)
            False #Ajouter la sortie console dans un fichier texte (Optionnel, Default: False)
        )
    )

print("\n--------------------------------------------------\n")