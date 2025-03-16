from hashlib import md5
# ЗАДАЧА
# есть три пароля: w1, w2. w3. Каждый состоит из 6 символов.
# Символы - только цифры и латинские буквы в верхнем и нижнем регистрах
# известно что:
# md5(w1.encode()).hexdigest() = b9e9e5e6bb679e91c43a229e9f21a37f
# md5(w2.encode()).hexdigest() = 20afc891efbd174d0cbb8f02bd49b587
# md5(w3.encode()).hexdigest() = 1a6de0f03d8c7578e4114ebc8c0f9fec
# а также что если
# check = word1 + " " + word2 + " " + word3
#
# md5(check.encode()).hexdigest() = 265ca39ad0ce090e790fc57e383ade73
# найдите w1, w2, w3.


import asyncio
import hashlib
import string
from concurrent.futures import ThreadPoolExecutor


# Заданные хэши
w1_hash = "b9e9e5e6bb679e91c43a229e9f21a37f"
w2_hash = "20afc891efbd174d0cbb8f02bd49b587"
w3_hash = "1a6de0f03d8c7578e4114ebc8c0f9fec"
check_hash = "265ca39ad0ce090e790fc57e383ade73"

# Символы для генерации паролей
symbols = string.ascii_letters + string.digits
print(symbols)


# Функция для проверки пароля
def check_password(password):
    return hashlib.md5(password.encode()).hexdigest() == w1_hash


# Генерация и проверка паролей
for c1 in symbols:
    for c2 in symbols:
        for c3 in symbols:
            for c4 in symbols:
                for c5 in symbols:
                    for c6 in symbols:
                        password = c1 + c2 + c3 + c4 + c5 + c6
                        if check_password(password):
                            print(f"Пароль найден: {password}")
                            exit()
