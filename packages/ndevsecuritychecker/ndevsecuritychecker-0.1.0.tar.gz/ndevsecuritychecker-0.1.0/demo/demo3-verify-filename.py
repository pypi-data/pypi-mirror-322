from src import dev_sec

# Variable nécessaire a la fonction

path = "C:\\Users\\iguille\\base-project-structure\\tests\\testpath"
file_extension = [".py", ".yaml", ".key"]
file_extension2 = [".ts", ".txt"]

naming_convention = "camel_case"
naming_convention2 = "snake_case"
naming_convention3 = "uppercase"

# Fonction principale
# Trois premiers parametres obligatoires ! Le chemin a vérifier, les extensions des fichiers et la convention de nommage des variables
print("Naming convention: uppercase\n")
dev_sec.print_result(
    dev_sec.retrieve_sensible_data(
            path, #Chemin a verifier (Obligatoire)
            file_extension,  #Extension des fichiers a verifier (Obligatoire)
            naming_convention3, #Convention de nommage des variables (Obligatoire)
            True, #Regarder directement si le nom du fichier est sensible ou non (Optionnel, Default: False)
            False, #Ajouter les fichiers sensibles au .gitignore (Optionnel, Default: False)
            True #Ajouter la sortie console dans un fichier texte (Optionnel, Default: False)
        )
    )

print("\n--------------------------------------------------\n")