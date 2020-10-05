import re
def upload_password(pass_str):
    if len(pass_str) > 4:
        return pass_str
    raise ValueError('Password is too short.') 

def user_password(pass_str):
    if len(pass_str) > 8 and re.search('[a-z]', pass_str) is not None \
        and re.search('[A-Z]', pass_str) is not None \
            and re.search('[0-9]', pass_str) is not None:
        return pass_str
    else:
        raise ValueError('Password has to be min. 8 chars length, contains lower letters, capital letters and digits')

def user_email(email_str):
    email_regex = '^\w+[\._]?\w+[@]\w+[.]\w{2,3}$'
    if re.search(email_regex, email_str) is not None:
        return email_str
    raise ValueError('Invalid email')

def user_login(login_str):
    login_regex = '^[a-zA-Z][a-zA-Z0-9]{3,90}$'
    if re.search(login_regex, login_str) is not None:
        return login_str
    raise ValueError('Invalid login. Login has to start with letter, contains only alphanumeric chars and has minimum 4 chars length.')

user_validators = {
    'user_password' : user_password,
    'user_email' : user_email,
    'user_login' : user_login
}