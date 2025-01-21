from src import dev_sec

# Variable nécessaire a la fonction

path = "C:\\Users\\iguille\\base-project-structure\\tests\\testpath"
file_extension = [".py", ".yaml"]
file_extension2 = [".ts", ".txt"]

naming_convention = "camel_case"
naming_convention2 = "snake_case"
naming_convention3 = "uppercase"

# Fonction principale
# Trois premiers parametres obligatoires ! Le chemin a vérifier, les extensions des fichiers et la convention de nommage des variables
print("Naming convention: camel_case\n")
dev_sec.print_result(dev_sec.retrieve_sensible_data(path, file_extension, naming_convention))

print("\n--------------------------------------------------\n")

print("Naming convention: snake_case\n")
dev_sec.print_result(dev_sec.retrieve_sensible_data(path, file_extension, naming_convention))

print("\n--------------------------------------------------\n")

print("Naming convention: uppercase\n")
dev_sec.print_result(dev_sec.retrieve_sensible_data(path, file_extension, naming_convention))

print("\n--------------------------------------------------\n")

#Differents extensions
print("Extension differents\n")
print("Naming convention: camel_case\n")
dev_sec.print_result(dev_sec.retrieve_sensible_data(path, file_extension, naming_convention))

print("\n--------------------------------------------------\n")

print("Naming convention: snake_case\n")
dev_sec.print_result(dev_sec.retrieve_sensible_data(path, file_extension, naming_convention))

print("\n--------------------------------------------------\n")

print("Naming convention: uppercase\n")
dev_sec.print_result(dev_sec.retrieve_sensible_data(path, file_extension, naming_convention))

print("\n--------------------------------------------------\n")