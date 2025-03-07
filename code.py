import requests
import re
import os
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def clear_screen():
    """Очищает экран консоли."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Отображает главное меню."""
    clear_screen()
    print("=" * 40)
    print("          ПОИСК И ПРОВЕРКА ДАННЫХ")
    print("=" * 40)
    print("1. Поиск профиля по нику")
    print("2. Проверить Gmail")
    print("3. Проверить номер телефона")
    print("4. История поиска")
    print("5. Поиск информации по IP")
    print("6. Выйти")
    print("=" * 40)

def check_profile_exists(url):
    """Проверяет наличие профиля по URL."""
    try:
        response = requests.get(url, allow_redirects=False, timeout=5)  # Таймаут 5 секунд
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"[-] Ошибка при проверке {url}: {e}")
        return False

def search_profiles(nickname):
    """Ищет профили по нику в социальных сетях."""
    print(f"\nПроверяем ник '{nickname}' в социальных сетях...")

    # Список социальных сетей для проверки
    social_networks = {
        "ВКонтакте": f"https://vk.com/{nickname}",
        "Instagram": f"https://www.instagram.com/{nickname}/",
        "Twitter": f"https://twitter.com/{nickname}",
        "GitHub": f"https://github.com/{nickname}",
        "Telegram": f"https://t.me/{nickname}",
        "TikTok": f"https://www.tiktok.com/@{nickname}",
        "Facebook": f"https://www.facebook.com/{nickname}",
        "LinkedIn": f"https://www.linkedin.com/in/{nickname}",
        "Reddit": f"https://www.reddit.com/user/{nickname}",
        "Pinterest": f"https://www.pinterest.com/{nickname}",
        "Twitch": f"https://www.twitch.tv/{nickname}",
        "YouTube": f"https://www.youtube.com/@{nickname}",
    }

    # Проверяем наличие профиля
    results = []
    for network, url in social_networks.items():
        if check_profile_exists(url):
            print(f"[+] Профиль найден в {network}: {url}")
            results.append(f"[+] {network}: {url}")
        else:
            print(f"[-] Профиль не найден в {network}")
            results.append(f"[-] {network}: не найден")

    # Сохраняем результаты в файл
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        history_file = os.path.join(current_dir, "search_history.txt")
        with open(history_file, "a", encoding="utf-8") as file:
            file.write(f"Поиск по нику: {nickname}\n")
            file.write("\n".join(results) + "\n\n")
    except PermissionError:
        print("[-] Ошибка: Нет прав на запись в файл search_history.txt.")
    except Exception as e:
        print(f"[-] Ошибка при сохранении истории: {e}")

    input("\nНажми Enter, чтобы вернуться в меню...")

def check_gmail(email):
    """Проверяет, существует ли аккаунт Gmail."""
    print(f"\nПроверяем Gmail: {email}...")

    # Проверка формата email
    if not re.match(r"[^@]+@gmail\.com", email):
        print("[-] Это не Gmail. Введите адрес в формате example@gmail.com.")
        input("\nНажми Enter, чтобы вернуться в меню...")
        return

    # Проверка существования email
    try:
        # Валидация email
        valid = validate_email(email)
        print(f"[+] Аккаунт Gmail существует: {email}")
    except EmailNotValidError as e:
        print(f"[-] Аккаунт Gmail не существует: {email}")
        print(f"    Ошибка: {e}")

    # Сохраняем результат в файл
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        history_file = os.path.join(current_dir, "search_history.txt")
        with open(history_file, "a", encoding="utf-8") as file:
            file.write(f"Проверка Gmail: {email}\n")
            file.write(f"Результат: {'существует' if valid else 'не существует'}\n\n")
    except PermissionError:
        print("[-] Ошибка: Нет прав на запись в файл search_history.txt.")
    except Exception as e:
        print(f"[-] Ошибка при сохранении истории: {e}")

    input("\nНажми Enter, чтобы вернуться в меню...")

def check_phone_number(phone):
    """Проверяет номер телефона с помощью AbstractAPI."""
    print(f"\nПроверяем номер телефона: {phone}...")

    # Проверка формата номера
    if not re.match(r"^\+?[0-9]{10,15}$", phone):
        print("[-] Неверный формат номера. Номер должен начинаться с '+' и содержать от 10 до 15 цифр.")
        print("    Пример правильного формата: +79161234567")
        input("\nНажми Enter, чтобы вернуться в меню...")
        return

    # Используем AbstractAPI для проверки номера
    api_key = "1771d4dfa1bb46c6922c204a175e1423"  # Ваш API-ключ
    url = f"https://phonevalidation.abstractapi.com/v1/?api_key={api_key}&phone={phone}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("valid"):
            print(f"[+] Номер {phone} валиден.")
            print(f"    Формат: {data['format']['international']}")
            print(f"    Страна: {data['country']['name']} ({data['country']['code']})")
            print(f"    Местоположение: {data.get('location', 'Неизвестно')}")
            print(f"    Тип: {data.get('type', 'Неизвестно')}")
            print(f"    Оператор: {data.get('carrier', 'Неизвестно')}")
        else:
            print(f"[-] Номер {phone} невалиден.")
    except Exception as e:
        print(f"[-] Ошибка при проверке номера: {e}")

    # Сохраняем результат в файл
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        history_file = os.path.join(current_dir, "search_history.txt")
        with open(history_file, "a", encoding="utf-8") as file:
            file.write(f"Проверка номера: {phone}\n")
            file.write(f"Результат: {'валиден' if data.get('valid') else 'невалиден'}\n\n")
    except PermissionError:
        print("[-] Ошибка: Нет прав на запись в файл search_history.txt.")
    except Exception as e:
        print(f"[-] Ошибка при сохранении истории: {e}")

    input("\nНажми Enter, чтобы вернуться в меню...")

def search_ip_info(ip):
    """Ищет информацию по IP-адресу."""
    print(f"\nПроверяем IP: {ip}...")

    # Используем API ip-api.com
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["status"] == "success":
            print(f"[+] Информация по IP {ip}:")
            print(f"    Страна: {data.get('country', 'Неизвестно')}")
            print(f"    Регион: {data.get('regionName', 'Неизвестно')}")
            print(f"    Город: {data.get('city', 'Неизвестно')}")
            print(f"    Провайдер: {data.get('isp', 'Неизвестно')}")
            print(f"    Организация: {data.get('org', 'Неизвестно')}")
            print(f"    Координаты: {data.get('lat', 'Неизвестно')}, {data.get('lon', 'Неизвестно')}")
        else:
            print(f"[-] Не удалось получить информацию по IP {ip}.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Ошибка при проверке IP: {e}")

    # Сохраняем результат в файл
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        history_file = os.path.join(current_dir, "search_history.txt")
        with open(history_file, "a", encoding="utf-8") as file:
            file.write(f"Проверка IP: {ip}\n")
            if data["status"] == "success":
                file.write(f"Результат: найдено\n")
                file.write(f"Страна: {data.get('country', 'Неизвестно')}\n")
                file.write(f"Город: {data.get('city', 'Неизвестно')}\n")
                file.write(f"Провайдер: {data.get('isp', 'Неизвестно')}\n\n")
            else:
                file.write(f"Результат: не найдено\n\n")
    except PermissionError:
        print("[-] Ошибка: Нет прав на запись в файл search_history.txt.")
    except Exception as e:
        print(f"[-] Ошибка при сохранении истории: {e}")

    input("\nНажми Enter, чтобы вернуться в меню...")

def search_history():
    """Показывает историю поиска."""
    print("\n" + "=" * 40)
    print("          ИСТОРИЯ ПОИСКА")
    print("=" * 40)
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        history_file = os.path.join(current_dir, "search_history.txt")
        with open(history_file, "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print("История поиска пуста.")
    except PermissionError:
        print("[-] Ошибка: Нет прав на чтение файла search_history.txt.")
    except Exception as e:
        print(f"[-] Ошибка при чтении истории: {e}")
    print("=" * 40)
    input("\nНажми Enter, чтобы вернуться в меню...")

def main():
    while True:
        display_menu()
        choice = input("Выбери действие (1-6): ")

        if choice == "1":
            nickname = input("Введи ник: ")
            search_profiles(nickname)

        elif choice == "2":
            email = input("Введи Gmail: ")
            check_gmail(email)

        elif choice == "3":
            phone = input("Введи номер телефона: ")
            check_phone_number(phone)

        elif choice == "4":
            search_history()

        elif choice == "5":
            ip = input("Введи IP-адрес: ")
            search_ip_info(ip)

        elif choice == "6":
            print("Выход из программы. Удачи!")
            break

        else:
            print("Неверный выбор. Попробуй еще раз.")
            input("Нажми Enter, чтобы продолжить...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    input("Нажми Enter, чтобы выйти...")
