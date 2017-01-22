import math
import string
import getpass

def blacklist_open():
    try:
        with open('blacklist.txt', 'r') as blacklist:
            return list(blacklist)
    except IOError:
        print("Не удалось найти файл blacklist.txt. "
            "Проверка по списку популярных паролей не будет выполнена.\n")
        return False


def blacklist_coincidence_check(password, blacklist):
    exist_in_blacklist = False
    if blacklist:
        for word in blacklist:
            if password.find(word.replace("\n","")) != -1:
                exist_in_blacklist = True   
    return exist_in_blacklist


def personal_data_coincidence_check(password, data):
    coincidence = [element for element in data.values() if element.lower() == password.lower()]
    return len(coincidence)


def total_charset_calculation(password):
    alpha = string.ascii_lowercase
    upper = string.ascii_uppercase
    upper_punct = string.punctuation
    digits = string.digits

    total_considered_ascii_chars = 0x7f - 0x20
    alpha_chars = len(alpha)
    upper_chars = len(upper)
    upper_punct_chars = len(upper_punct)
    digit_chars = len(digits)
    other_chars = total_considered_ascii_chars - \
    (alpha_chars + upper_chars + upper_punct_chars + digit_chars)
    
    total_charset = 0.
    
    for symbol in password:
        if symbol in alpha:
            total_charset += alpha_chars
        elif symbol in upper:
            total_charset += upper_chars
        elif symbol in upper_punct:
            total_charset += upper_punct_chars
        elif symbol in digits:
            total_charset += digit_chars
        else:
            total_charset += other_chars

    return total_charset


def strength_calculation(password):
    
    max_pass_value = 10
    value_for_high_strength = 100
    step_of_decrease_strength = value_for_high_strength / max_pass_value 
    
    total_charset = total_charset_calculation(password)
    pass_strength = math.log(total_charset, math.e) * (len(password) / math.log(2, math.e))
    

    if pass_strength >= value_for_high_strength:
        return max_pass_value
    else:    
        return pass_strength//step_of_decrease_strength


def total_calculation(password, personal_data):
    if blacklist_coincidence_check(password, blacklist_open()):
        blacklist_modifier = -2
    else:
        blacklist_modifier = 0

    personal_data_coincidence = personal_data_coincidence_check(password, personal_data)
    if personal_data_coincidence >= 2:
        personal_data_coincidence_modifier = -3
    elif personal_data_coincidence == 1:
        personal_data_coincidence_modifier = -2
    else:
        personal_data_coincidence_modifier = 0

    total_pass_strength = int(strength_calculation(password) +\
    blacklist_modifier + personal_data_coincidence_modifier)

    return max(total_pass_strength, 0)


def collecting_personal_data():
    personal_data = {}
    print("Добрый день!\nПросьба идентифицироваться.")
    '''personal_data['name'], personal_data['surname'] = input("Введите своё имя и фамилию:").split()
    personal_data['birthday'] = ''.join(input("Введите дату своего рождения в формате ДД.ММ.ГГГГ:").split('.'))
    personal_data['tel_num'] = ''.join(input("Введите номер своего телефона:").split(' '))
    personal_data['name_org'] = ''.join(input("Введите название своей компании:").split(' '))
    personal_data['short_name_org'] = ''.join(input("Введите сокращенное название своей компании:").split(' '))
    '''
    personal_data['user_login'] = input("Введите ваш логин:")
    return personal_data


if __name__ == '__main__':

    personal_data = collecting_personal_data()

    while True:
        user_password = getpass.getpass("Введите ваш пароль для проверки сложности: ")
        total_pass_strength = total_calculation(user_password, personal_data)

        print("\nСложность вашего пароля: %s" % total_pass_strength)
        if total_pass_strength >= 6:
            choice = input("Ваш пароль обладает достаточной сложностью. "\
                            "Если хотите использовать его, нажмите Y, "\
                            "если хотите ввести другой пароль, введите любой текст: ")
            if choice == 'Y':
                break
        else:
            print("Ваш пароль недостаточно сложный, просьба придумать новый пароль.")
