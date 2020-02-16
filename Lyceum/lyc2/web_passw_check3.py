import re

ENG = "qwertyuiopasdfghjklzxcvbnm"
RUS = "йцукенгшщзхъфывапролджэячсмитьбю"

passwd = input('Введите пароль: ')


def check_len(p):
    assert len(p) > 8


def check_letters(p):
    if not re.search('[A-ZА-Я]', p) and re.search('[a-zа-я]', p):
        raise AssertionError


def check_number(p):
    if not re.search('[0-9]', p):
        raise AssertionError


def check_klawa(p):
    for i in range(0, len(p) - 2):
        if p[i:i + 2].lower() in ENG or p[i:i + 2].lower() in RUS:
            raise AssertionError


flag = True
for func in (check_len, check_letters, check_number, check_klawa):
    try:
        func(passwd)
    except AssertionError as a:
        flag = False


if flag:
    print('ok') 
else:
    print('error')
