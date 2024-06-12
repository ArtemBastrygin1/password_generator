import secrets
import string
import logging


def get_user_preferences():
    length = int(input("Введите длину вашего пароля: "))
    include_letters = input("Включать буква? (да/нет): ").lower().strip() == 'да'
    include_digits = input("Включать цифры? (да/нет): ").lower().strip() == 'да'
    include_special = input("Включать спецсимволы? (да/нет): ").lower().strip() == 'да'
    mask_password = input("Желаете ли вы после замаскировать свой пароль? (да/нет): ").lower().strip() == 'да'
    return length, include_letters, include_digits, include_special, mask_password


def generate_password(length, include_letters, include_digits, include_special):
    symbols_base = ''
    if include_letters:
        symbols_base += string.ascii_letters
    if include_digits:
        symbols_base += string.digits
    if include_special:
        symbols_base += string.punctuation

    if not symbols_base:
        raise ValueError("Необходимо выбрать хотя бы один тип символов!")

    password = ''.join(secrets.choice(symbols_base) for _ in range(length))
    return password


def save_password_to_file(password):
    logging.info(f"Generated password: {password}")


def assess_password_strength(password):
    length = len(password)
    has_letters = any(c.isalpha() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = 0
    if length >= 8:
        score += 1
    if has_letters:
        score += 1
    if has_digits:
        score += 1
    if has_special:
        score += 1

    return score


def main():
    length, include_letters, include_digits, include_special, mask_password = get_user_preferences()
    try:
        password = generate_password(length, include_letters, include_digits, include_special)
        if mask_password:
            masked_password = '*' * len(password)
            print(f'Готово! Ваш сгенерированный пароль: {masked_password}')
        else:
            print(f'Готово! Ваш сгенерированный пароль: {password}')

        if input("Сохранить пароль в файл? (да/нет): ").lower().strip() == 'да':
            save_password_to_file(password)
            print("Успешно! Пароль сохранен в файл 'password.log'.")

        if input("Оценить сложность пароля? (да/нет): ").lower().strip() == 'да':
            score = assess_password_strength(password)
            complexity = ["Очень слабый", "Слабый", "Средний", "Сложный", "Очень сложный"]
            print(f'Сложность пароля: {complexity[score]} ({score}/4)')
    except ValueError as e:
        print(f'Ошибка: {e}')


if __name__ == "__main__":
    logging.basicConfig(
        filename="passwords.log",
        level=logging.INFO,
        format='%(message)s (Date: %(asctime)s)',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    try:
        main()
    except KeyboardInterrupt:
        print("\nДо свидания, спасибо, что пользуетесь программой!")
        exit()
