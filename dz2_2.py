# [ ] Написати скрипт dz2_2.py, який використовуючи bash команди через subprocess буде:
# * Копіювати файл dz1.py в файл dz1_run.py
# * Дописувати в початок файлу dz1_run.py з bash (можна без subprocess)
# * Змінювати права на файл:
# * Доступ повністю заборонено для всіх крім овнера
# * Овнер може читати і запускати файл
# * Запускати `dz1_run.py`

import subprocess
import os

if not os.path.exists('dz1.py'):
    print("File dz1.py was not found!")
    exit(1)

try:
    subprocess.run(['cp', 'dz1.py', 'dz1_run.py'], check=True)
    print("File dz1.py is successfully copied to dz1_run.py")
except subprocess.CalledProcessError as e:
    print(f"Error while coping the file: {e}")
    exit(1)

prepend_text = "#!/usr/bin/env python3\n# File for execution\n\n"
try:
    if not os.path.exists("dz1_run.py"):
        print("File dz1_run.py was not found!")
        exit(1)

    with open("dz1_run.py", "r+") as file:
        original_content = file.read()
        file.seek(0)
        file.write(prepend_text + original_content)
    print("Text is successfully added to the beginning of dz1_run.py")
except Exception as e:
    print(f"Error while changing file: {e}")
    exit(1)

try:
    if not os.path.exists("dz1_run.py"):
        print("File dz1_run.py was not found!")
        exit(1)

    subprocess.run(['chmod', '700', 'dz1_run.py'], check=True)
    print("File rights are changed: owner only has access")
except subprocess.CalledProcessError as e:
    print(f"Error while changing file rights: {e}")
    exit(1)

try:
    if not os.path.exists("dz1_run.py"):
        print("File dz1_run.py was not found!")
        exit(1)

    subprocess.run(['./dz1_run.py'], check=True)
    print("File dz1_run.py was successfully executed")
except subprocess.CalledProcessError as e:
    print(f"Error while executing dz1_run.py: {e}")
    exit(1)

except Exception as e:
    print(f"Unknown error: {e}")
    exit(1)
