"""
Dev_Utils security section, 
in here you'll found all functions related to the security features of the module
"""
#TODO: Add Types to all variables in the file

from datetime import datetime
from src import sec_names #FOR PYTEST ONLY
from rich import print
#import logging
#import sec_names
import os 

# logger = logging.getLogger(__name__)
# logging.basicConfig(filename="dev_utils.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def _check_path_validity(path: str) -> bool:
    """
    Check if the given path is valid and if the path syntax is correct.

    :param path (string): The path to check.
    :return (bool): True if the path is valid, False otherwise.
    """
    invalid_chars = [" ", "²", "&", "'", ">", "<", ";", '"'] #TODO: Can add more here

    for char in invalid_chars:
        if char in path:
            print(f"[red]PathError: Path syntax contain an invalid char'{char}'[/red]")
            return False

    if not os.path.exists(path):
        print("[red]PathError: No such path[/red]")
        return False
    return True

def _check_extension_validity(file_extension_to_verify: list[str]) -> TypeError:
    """
    Check if all elements in the file_extension_to_verify list are strings.

    :param file_extension_to_verify (list[str]): List of file extensions to verify.
    :return (bool): True if all elements are strings, False if there is a TypeError.
    """
    for verified_element in file_extension_to_verify:
        if isinstance(verified_element, str) and ".gitignore" not in verified_element:
            return True
            continue
        else:
            print("[red]TypeError: File extension must be a string and different from .gitignore[/]")
            return False

def _get_files_to_analyze(path: str, file_extensions: list[str]) -> list:
    """
    Go trough every folders and files in a specified directory 
    and add files of the correct extension to a list 

    :param path (string): the path to analyse
    :param file_extension (list): the file extensions to allow in 
    :return: return the list of the files
    """
    path = os.path.abspath(path)
    files_to_check = []
    extension_set = set(file_extensions)

    if _check_path_validity(path) and _check_extension_validity(file_extensions):
        for dirpath, _, files in os.walk(path):
            files_to_check.extend(dirpath + "\\" + file for file in files if file.endswith(tuple(extension_set)))
    else:
        print("[bold red]Error: Cannot get files: Path or extension not valid ![/]")

    return files_to_check

def _clean_result(main_function_result: list[str]) -> list:
    cleaned_result = []

    for line in main_function_result:
        line = line.replace("[bold red]", "")
        line = line.replace("[cyan]", "")
        line = line.replace("[blue]", "")
        line = line.replace("[yellow]", "")
        line = line.replace("[/]", "")
        cleaned_result.append(line)
    
    return cleaned_result

def _add_result_in_file(content: list[str], filename: str) -> None:
    """
    Add the result of retrieve_sensible_data() to an output .txt file
    :param content (list[str]): should be the result of retrieve_sensible_data()
    :param filename (str): file name for output file 
    """
    verification_time = datetime.now()

    try:
        with open(os.getcwd() + "\\" + filename, "w") as output_file:
            output_file.write(f"Verification time: {verification_time.strftime('%Y-%m-%d %H:%M:%S')} \n\n")
            for line in content:
                output_file.write(line + "\n")
            return True
    except:
        print("[red]WriteError: Cannot write in output file.[/]")
        return False

def _search_for_gitrepo(path: str) -> str:
    """
    Search for the .git folder in the given path.

    This function will climb up the directory tree until it finds a .git folder or reaches the root of the drive.
    If it doesn't find a .git folder after 10 tries it will return "error".
    :param path (str): The path to search in.
    :return (str): The path to the .git folder if found, "error" if not.
    """
    max_tries = 10
    tries = 0

    while tries < max_tries:
        if os.path.exists(os.path.join(path, ".git")):
            return path

        parent_dir = os.path.dirname(path)
        if parent_dir == path:
            break

        path = parent_dir
        tries += 1

    print(f"[red]PathError: Cannot find .git folder | Folder depth level is set to {max_tries}[/]")
    return "error"

def _process_path_for_gitignore(path: str, filepath_to_process: list[str]) -> str:
    """
    Processes a list of file paths to create paths relative to the git repository root,
    and formats them for inclusion in a .gitignore file.

    :param path (str): The path to the git repository.
    :param filepath_to_process (list[str]): A list of file paths to process.
    :return (list[str]): A list of processed file paths formatted for .gitignore.
    """

    paths_proccessed = []
    git_repo_path = _search_for_gitrepo(path)

    for filepath in filepath_to_process:
        filepath = filepath[1 + len(git_repo_path):]
        filepath = filepath.replace("\\", "/")
        filepath = filepath.replace(" ", "")

        paths_proccessed.append(filepath)

    return paths_proccessed

def _write_in_gitignore(gitignore_path: str, files_to_ignore: list[str], write_mode: str) -> None:
    """
    Write a list of files to the .gitignore file in the specified mode.

    :param gitignore_path (str): The path to the .gitignore file.
    :param files_to_ignore (list[str]): A list of file paths to add to .gitignore.
    :param write_mode (str): The mode to open the file ('a' for append, 'x' for exclusive creation).
    :return: None
    """
    with open(gitignore_path, write_mode) as gitignore_file:
        gitignore_file.write("\n\n#Detected Sensible Files\n")

        for line in _process_path_for_gitignore(gitignore_path, files_to_ignore):
            gitignore_file.write(line + "\n")

def _add_files_to_ignore(path: str, files_to_ignore: list[str]) -> bool:
    """
    Add sensible files to the .gitignore file of the given path if the path is a git repository.
    
    :param path (str): The path to the git repository.
    :param file (list[str]): The list of files to add to the .gitignore file.
    :return (bool): True if the file has been added to the .gitignore file, False otherwise.
    """
    path = os.path.abspath(path)
    gitignore_path = _search_for_gitrepo(path)

    if not _check_path_validity(path) and not os.path.isdir(path):
        return False

    if os.path.exists(gitignore_path):
        _write_in_gitignore(gitignore_path + "\\.gitignore", files_to_ignore, "a")
    else:
         _write_in_gitignore(gitignore_path + "\\.gitignore", files_to_ignore, "x")
 
def retrieve_sensible_data(
        path: str, 
        file_extensions: list[str], 
        naming_convention: str, 
        check_file_name: bool=False,
        add_to_gitignore: bool=False,
        output_to_file: bool=False
    ) -> list:
    """
    Retrieve any sensible data in files of the specified type.

    :param file_extensions (list): the file extensions to check
    :param path (string): the path to check
    :param naming_convention (string): the naming convention for variables used in your project
    :param check_file_name (bool): whether to check the file name or not (default: False)
    :param add_to_gitignore (bool): whether to add the file to the .gitignore file or not (default: False)
    :return (list[str]): a list of the file where a sensible data was found
    """

    output_filename = "retrieved_sensible_data.txt"
    files_to_check = _get_files_to_analyze(path, file_extensions)
    detected_files = []
    result = []

    if check_file_name:
        for file in files_to_check:
            found_file_words = [word for word in sec_names.sensible_data_variables[naming_convention] if word in file]
            if found_file_words:
                result.append(f"[bold red]In file[/] [cyan]{file}[/][bold red]: Detected sensitive file name[/]")
                detected_files.append(file)

    for file in files_to_check:
        with open(file, "r") as file_content:
            for line_number, line in enumerate(file_content):
                found_words = [word for word in sec_names.sensible_data_variables[naming_convention] if word in line]
                if found_words and file not in detected_files:
                    result.append(f"[bold red]In file[/] [cyan]{file}[/][bold red] at line [blue]{line_number + 1}[/][bold red]: Found sensitive data: [yellow]{found_words}[/]")

    if output_to_file: _add_result_in_file(_clean_result(result), output_filename)
    if add_to_gitignore: _add_files_to_ignore(path, files_to_check)
    
    return result

def print_result(result: list[str]) -> None:
    """
    Print the result of the get file to analyse

    :param result (list): WARNING: SHOULD TAKE ONLY THE RESULT OF THE retrieve_sensible_data() FUNCTION
    """
    for line in result:
        print(line)