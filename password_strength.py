import math

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
        print('Не удалось найти файл blacklist.txt. Проверка по списку популярных паролей не будет выполнена.\n\n')
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

def basic_algorithm(password):
    alpha = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    upper_punct = "~`!@#$%^&*()-_+="
    digits = "1234567890"

    totalChars = 0x7f - 0x20 # Символы с 32 по 127 таблицы ASCII. Это множество включает в себя строчные и заглавные буквы латиницы, цифры и набор спецсимволов.
    alphaChars = len(alpha)
    upperChars = len(upper)
    upper_punctChars = len(upper_punct)
    digitChars = len(digits)
    otherChars = totalChars - (alphaChars + upperChars + upper_punctChars + digitChars) 

    # Ниже следуют переменные, показывающие наличие групп символов в пароле.
    alpha_exists = False
    upper_exists = False
    upperPunct_exists = False
    digit_exists = False
    other_exists = False

# Проверка на то к какой группе относится символ из пароля.
    for symbol in password:
        if symbol in alpha:
            alpha_exists = True
        elif symbol in upper:
            upper_exists = True
        elif symbol in upper_punct:
            upperPunct_exists = True
        elif symbol in digits:
            digit_exists = True
        else:
            other_exists = True

    charset = 0 # Cуммарный размер множеств используемых символов.

# Если в пароле присутствует символ из определенной группы, увеличиваем значение charset на размер этой группы.
    if alpha_exists:
        charset += alphaChars
    if upper_exists:
        charset += upperChars
    if upperPunct_exists:
        charset += upper_punctChars
    if digit_exists:
        charset += digitChars
    if other_exists:
        charset += otherChars

# Для оценки стойкости используем формулу strength = ln(charset) * len(password) / ln(e)
    pass_strength_ba = math.log(charset, math.e) * (len(password) / math.log(2, math.e))
    if pass_strength_ba >= 100:
        return 10
    else:    
        return pass_strength_ba//10

def strength_calculation(password, personal_data):
    pass_strength = float(basic_algorithm(password))+ float(blacklist_check(password)) + float(data_check(password, personal_data))
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
