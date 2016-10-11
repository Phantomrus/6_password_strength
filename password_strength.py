import math
import string

def blacklist_check(password):
    exist_in_blacklist = False
    try:
        with open('blacklist.txt', 'r') as blacklist:
            for word in blacklist.readlines():
                if password.find(word) != -1:
                    exist_in_blacklist = True
        if exist_in_blacklist:
            return -2
        else:
            return 0
    except IOError:
        print('Не удалось найти файл blacklist.txt. Проверка по списку популярных паролей не будет выполнена.\n')
        return 0

def data_check(password, data):
    pass_include_personal = 0
    for element in data:
        if element in password:
            pass_include_personal += 1
    if pass_include_personal >= 2:
        return -3
    elif pass_include_personal == 1:
        return -2
    else:
        return 0

def total_charset_definition(password):
    alpha = string.ascii_lowercase
    upper = string.ascii_uppercase
    upper_punct = string.punctuation
    digits = string.digits

    total_considered_ascii_chars = 0x7f - 0x20 # Символы с 32 по 127 таблицы ASCII. Это множество включает в себя строчные и заглавные буквы латиницы, цифры и набор спецсимволов.
    alpha_chars = len(alpha)
    upper_chars = len(upper)
    upper_punct_chars = len(upper_punct)
    digit_chars = len(digits)
    other_chars = total_considered_ascii_chars - (alpha_chars + upper_chars + upper_punct_chars + digit_chars) 

    # Ниже следуют переменные, показывающие наличие групп символов в пароле.
    alpha_exists = False
    upper_exists = False
    upper_punct_exists = False
    digit_exists = False
    other_exists = False

# Проверка на то к какой группе символов относится символ из пароля.
    for symbol in password:
        if symbol in alpha:
            alpha_exists = True
        elif symbol in upper:
            upper_exists = True
        elif symbol in upper_punct:
            upper_punct_exists = True
        elif symbol in digits:
            digit_exists = True
        else:
            other_exists = True

    total_charset = 0 # Cуммарный размер множеств используемых символов.

# Если в пароле присутствует символ из определенной группы, увеличиваем значение total_charset на размер этой группы.
    if alpha_exists:
        total_charset += alpha_chars
    if upper_exists:
        total_charset += upper_chars
    if upper_punct_exists:
        total_charset += upper_punct_chars
    if digit_exists:
        total_charset += digit_chars
    if other_exists:
        total_charset += other_chars

    return total_charset

def strength_definition(password):
    # Для оценки стойкости используем формулу strength = ln(total_charset) * len(password) / ln(e). Описание в readme.
    total_charset = total_charset_definition(password)
    pass_strength_ba = math.log(total_charset, math.e) * (len(password) / math.log(2, math.e))
    if pass_strength_ba >= 100:
        return 10
    else:    
        return pass_strength_ba//10

def strength_calculation(password, personal_data):
    pass_strength = float(strength_definition(password))+ float(blacklist_check(password)) + float(data_check(password, personal_data))
    if pass_strength <= 0:
        return 0
    else:
        return pass_strength


if __name__ == '__main__':

    print("Добрый день!\nПросьба идентифицироваться.")
    name, surname = input("Введите своё имя и фамилию:").split()
    date = input("Введите дату своего рождения в формате ДД.ММ.ГГГГ:")
    tel_num = input("Введите номер своего телефона:")
    name_org = input("Введите название своей компании:")
    short_name_org = input("Введите сокращенное название своей компании:")
    user_login = input("Введите ваш логин:")

    date_for_check = ''.join(date.split('.'))
    name_org_for_check = ''.join(name_org.split(' '))
    short_name_org_for_check = ''.join(short_name_org.split(' '))
    personal_data = [name.lower(), surname.lower(), date_for_check, tel_num, name_org_for_check.lower(), short_name_org_for_check.lower(), user_login.lower()]

    while True:
        user_password = input("Введите ваш пароль для проверки сложности: ")
        pass_strength = strength_calculation(user_password.lower(), personal_data)

        print("\nСложность вашего пароля: %s" % pass_strength)
        if pass_strength >= 6:
            choice = input("Ваш пароль обладает достаточной сложностью. Если хотите использовать его, нажмите Y, если хотите ввести другой пароль, введите любой текст: ")
            if choice == 'Y':
                break
        else:
            print("Ваш пароль недостаточно сложный, просьба придумать новый пароль.")
