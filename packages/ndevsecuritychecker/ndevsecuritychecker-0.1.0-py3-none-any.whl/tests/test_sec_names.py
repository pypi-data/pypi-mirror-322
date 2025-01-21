from src import sec_names

def test_add_variables():
    assert sec_names.add_new_sensible_var_name("test_new_var_name_snake_case", "snake_case") == True 
    assert sec_names.add_new_sensible_var_name("test_new_var_name_uppercase", "uppercase") == False
    assert sec_names.add_new_sensible_var_name("TEST_NEW_VAR_NAME_UPPERCASE", "uppercase") == True
    assert sec_names.add_new_sensible_var_name("TestNewVarNameCamelCase", "camel_case") == True
    assert sec_names.add_new_sensible_var_name("TestNewVarNameCamelCase", "snake_case") == False
    assert sec_names.add_new_sensible_var_name("TestNewVarNameCamelCase", "uppercase") == False