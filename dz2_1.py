#Написати скрипт на python dz2_1.py, який використовуючи bash команди через subprocess буде:
 # * Виводити ім’я поточного користувача
  #* Виводити шлях до поточної директорії
  #* Створювати папку dz1 в поточній директорії
  #* В папці dz1 створювати файли для кожного дня поточного місяця в форматі `dd-mm-yyyy.log`(список назв має бути згенеровано за допомогою python генератора та модулю datetime)
  #* Змінювати овнера папки dz1 та всіх файлів в ній на root
  #* Видаляти 5 випадкових файлів з папки dz1
import os
import subprocess
import datetime
import random


def run_bash_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}")


def get_current_user():
    return subprocess.run("whoami", capture_output=True, text=True).stdout.strip()


def get_current_directory():
    return subprocess.run("pwd", capture_output=True, text=True).stdout.strip()


def create_directory():
    dir_name = "dz1"
    if not os.path.exists(dir_name):
        run_bash_command(f"mkdir {dir_name}")


def create_log_files():
    current_date = datetime.date.today()
    days_in_month = (datetime.date(current_date.year, current_date.month + 1, 1) -
                     datetime.date(current_date.year, current_date.month, 1)).days

    for day in range(1, days_in_month + 1):
        filename = f"dz1/{day:02d}-{current_date.month:02d}-{current_date.year}.log"
        with open(filename, 'w') as f:
            f.write(f"Log file for {day:02d}-{current_date.month:02d}-{current_date.year}")


def change_owner_to_root():
    run_bash_command("sudo chown -R root:root dz1")


def delete_random_files():
    files = os.listdir("dz1")
    random_files = random.sample(files, min(5, len(files)))
    for file in random_files:
        os.remove(os.path.join("dz1", file))
        print(f"Deleted file: dz1/{file}")


def main():

    user = get_current_user()
    print(f"Current user: {user}")

    current_dir = get_current_directory()
    print(f"Current directory: {current_dir}")

    create_directory()

    create_log_files()

    change_owner_to_root()

    delete_random_files()


if __name__ == "__main__":
    main()
