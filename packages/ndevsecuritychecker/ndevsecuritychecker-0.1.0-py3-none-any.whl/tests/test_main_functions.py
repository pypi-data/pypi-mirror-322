"""
This test only works on the H119 PC, 
"""

from src import dev_sec as ds

path = "C:\\Users\\iguille\\base-project-structure\\tests\\testpath"
longpath = "tests\\testpath\\1\\2\\3\\4\\5\\6\\7\\8\\9\\10"
error_path = "C:\\Users\\iguille\\base project structure\\tests\\testpath"

file_extension = [".py", ".yaml"]
file_extension_wrong = [4, ".py"]

test_content = ["15", "588848", "88", "558548"]

def test_check_path_validity():
    assert ds._check_path_validity(path) == True
    assert ds._check_path_validity(longpath) == True
    assert ds._check_path_validity(error_path) == False

def test_get_file_function():
    assert ds._get_files_to_analyze(path, file_extension) == [
    'C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file1.yaml', 'C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file2.py']
    assert ds._get_files_to_analyze(path, file_extension_wrong) == []

def test_add_result_in_file():
    assert ds._add_result_in_file(test_content, "test_file.txt") == True

def test_search_for_gitrepo():
    assert ds._search_for_gitrepo(path) == "C:\\Users\\iguille\\base-project-structure"
    assert ds._search_for_gitrepo(longpath) == "error"

def test_process_path():
    assert ds._process_path_for_gitignore(path, ["C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file1.yaml"]) == ['tests/testpath/test_file1.yaml']
    assert ds._process_path_for_gitignore(path, ["C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file .yaml"]) == ['tests/testpath/test_file.yaml']
    assert ds._process_path_for_gitignore(path, ["C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file45 .py"]) == ['tests/testpath/test_file45.py']
    assert ds._process_path_for_gitignore(path, ["C:/Users/iguille/base-project-structure/tests/testpath/test_file45 .yaml"]) == ['tests/testpath/test_file45.yaml']

def test_retreive_sensible_data():
    assert ds.retrieve_sensible_data(path, file_extension, "snake_case") == [
    "[bold red]In file[/] [cyan]C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file1.yaml[/][bold red] at line [blue]4[/][bold red]: Found sensitive data: [yellow]['password'][/]",
    "[bold red]In file[/] [cyan]C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file2.py[/][bold red] at line [blue]13[/][bold red]: Found sensitive data: [yellow]['api_key', 'key'][/]",
    "[bold red]In file[/] [cyan]C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file2.py[/][bold red] at line [blue]14[/][bold red]: Found sensitive data: [yellow]['api_secret', 'secret'][/]",
    "[bold red]In file[/] [cyan]C:\\Users\\iguille\\base-project-structure\\tests\\testpath\\test_file2.py[/][bold red] at line [blue]15[/][bold red]: Found sensitive data: [yellow]['session_key', 'key'][/]",
    ]
