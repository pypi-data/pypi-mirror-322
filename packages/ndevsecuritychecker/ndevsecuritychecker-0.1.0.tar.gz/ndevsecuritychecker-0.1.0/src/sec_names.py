"""
This file contains all the variable of the possible sensible data in files
multiple formats are in the file: CamelCase, snake_case, uppercase.

For now this is okay, if you want more case checks, just modify the package or ask me on Gitlab
"""
from rich import print

sensitive_data_vars_uppercase = [
    "API_KEY", "API_SECRET", "API_TOKEN", "API_KEY_ID", "API_SECRET_KEY", "ACCESS_TOKEN",
    "SECRET_KEY", "APP_API_KEY", "SERVICE_API_KEY", "AUTH_KEY", "CLIENT_SECRET", "CLIENT_ID",
    "PASSWORD", "USER_PASSWORD", "DB_PASSWORD", "ADMIN_PASSWORD", "SECRET_PASSWORD", "AUTH_PASSWORD",
    "LOGIN_PASSWORD", "PASSWORD_HASH", "ENCRYPTED_PASSWORD", "ROOT_PASSWORD", "AUTH_TOKEN",
    "AUTH_HEADER", "BEARER_TOKEN", "SESSION_KEY", "OAUTH_TOKEN", "JWT_TOKEN", "JWT_SECRET",
    "REFRESH_TOKEN", "ACCESS_KEY", "SECRET_ACCESS_KEY", "DB_USERNAME", "DB_PASSWORD", "DB_HOST",
    "DB_PORT", "DB_NAME", "DB_URI", "DB_CONNECTION_STRING", "DB_USER", "DATABASE_PASSWORD",
    "CREDENTIALS", "SECRET", "PRIVATE_KEY", "PRIVATE_SECRET", "CLIENT_SECRET_KEY", "ENCRYPTION_KEY",
    "SIGNING_KEY", "DECRYPTION_KEY", "APP_SECRET", "API_CREDENTIALS", "SERVICE_CREDENTIALS",
    "SMTP_PASSWORD", "SMTP_USERNAME", "SMTP_SERVER", "MAIL_PASSWORD", "MAIL_USERNAME", "EMAIL_PASSWORD",
    "EMAIL_API_KEY", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN", "GCP_API_KEY",
    "GCP_PROJECT_ID", "GCP_SERVICE_ACCOUNT_KEY", "AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID",
    "KEY", "SECRET_VALUE", "ENCRYPTION_SECRET", "HMAC_KEY", "SALT", "SESSION_SECRET"
]

sensitive_data_vars_camel_case = [
    "ApiKey", "ApiSecret", "ApiToken", "ApiKeyId", "ApiSecretKey", "AccessToken",
    "SecretKey", "AppApiKey", "ServiceApiKey", "AuthKey", "ClientSecret", "ClientId",
    "Password", "UserPassword", "DbPassword", "AdminPassword", "SecretPassword", "AuthPassword",
    "LoginPassword", "PasswordHash", "EncryptedPassword", "RootPassword", "AuthToken",
    "AuthHeader", "BearerToken", "SessionKey", "OauthToken", "JwtToken", "JwtSecret",
    "RefreshToken", "AccessKey", "SecretAccessKey", "DbUsername", "DbPassword", "DbHost",
    "DbPort", "DbName", "DbUri", "DbConnectionString", "DbUser", "DatabasePassword",
    "Credentials", "Secret", "PrivateKey", "PrivateSecret", "ClientSecretKey", "EncryptionKey",
    "SigningKey", "DecryptionKey", "AppSecret", "ApiCredentials", "ServiceCredentials",
    "SmtpPassword", "SmtpUsername", "SmtpServer", "MailPassword", "MailUsername", "EmailPassword",
    "EmailApiKey", "AwsAccessKeyId", "AwsSecretAccessKey", "AwsSessionToken", "GcpApiKey",
    "GcpProjectId", "GcpServiceAccountKey", "AzureClientId", "AzureClientSecret", "AzureTenantId",
    "Key", "SecretValue", "EncryptionSecret", "HmacKey", "Salt", "SessionSecret"
]

sensitive_data_vars_snake_case = [
    "api_key", "api_secret", "api_token", "api_key_id", "api_secret_key", "access_token",
    "secret_key", "app_api_key", "service_api_key", "auth_key", "client_secret", "client_id",
    "password", "user_password", "db_password", "admin_password", "secret_password", "auth_password",
    "login_password", "password_hash", "encrypted_password", "root_password", "auth_token",
    "auth_header", "bearer_token", "session_key", "oauth_token", "jwt_token", "jwt_secret",
    "refresh_token", "access_key", "secret_access_key", "db_username", "db_password", "db_host",
    "db_port", "db_name", "db_uri", "db_connection_string", "db_user", "database_password",
    "credentials", "secret", "private_key", "private_secret", "client_secret_key", "encryption_key",
    "signing_key", "decryption_key", "app_secret", "api_credentials", "service_credentials",
    "smtp_password", "smtp_username", "smtp_server", "mail_password", "mail_username", "email_password",
    "email_api_key", "aws_access_key_id", "aws_secret_access_key", "aws_session_token", "gcp_api_key",
    "gcp_project_id", "gcp_service_account_key", "azure_client_id", "azure_client_secret", "azure_tenant_id",
    "key", "secret_value", "encryption_secret", "hmac_key", "salt", "session_secret"
]


sensible_data_variables = {
    "camel_case": sensitive_data_vars_camel_case,
    "snake_case": sensitive_data_vars_snake_case,
    "uppercase": sensitive_data_vars_uppercase
}

def _verify_user_added_var_names(user_varname: str, convention: str) -> bool:
    """
    Verify if a user-provided variable name follows the guidelines of a given naming convention

    :param user_varname (str): the variable name to verify
    :param convention (str): the naming convention to check against
    :return (bool): True if the variable name follows the guidelines, False otherwise
    """
    match convention:
        case "camel_case":
            if user_varname[0].isupper() and "_" not in user_varname:
                return True
        case "snake_case":
            if user_varname.islower() and "_" in user_varname:
                return True
        case "uppercase":
            if user_varname.isupper() and "_" in user_varname:
                return True
        case _:
            print("[red]Your variable name does not follow any of the conventions guidelines[/red]")
            return False

def add_new_sensible_var_name(user_varname: str, convention: str) -> bool:
    """
    Add a user-provided variable name to the list of sensitive data variables for a given naming convention.

    :param user_varname (str): The variable name to add.
    :param convention (str): The naming convention to which the variable name should adhere.
    :return (bool) ONLY FOR UNIT TEST: True if the variable name was successfully added, False otherwise.
    """

    if _verify_user_added_var_names(user_varname, convention):
        sensible_data_variables[convention].append(user_varname)
        return True
    else:
        return False
    