import asyncio
import string
import hashlib
from concurrent.futures import ThreadPoolExecutor

symbols = string.ascii_letters + string.digits  # Символы для генерации паролей


def check_password(password, my_hash):
    return hashlib.md5(password.encode()).hexdigest() == my_hash


def check_passwords(c1, my_hash):
    for c2 in symbols:
        for c3 in symbols:
            for c4 in symbols:
                for c5 in symbols:
                    for c6 in symbols:
                        password = c1 + c2 + c3 + c4 + c5 + c6
                        if check_password(password, my_hash):
                            print(f"Пароль для {my_hash} найден: {password}")
                            return


async def async_check_passwords(c1, my_hash):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=1000) as pool:
        await loop.run_in_executor(pool, check_passwords, c1, my_hash)


async def main(my_hash):
    tasks = [async_check_passwords(c1, my_hash) for c1 in symbols]
    await asyncio.gather(*tasks)

if __name__ == "__main__":

    w1_hash = {"b9e9e5e6bb679e91c43a229e9f21a37f","20afc891efbd174d0cbb8f02bd49b587",
               "1a6de0f03d8c7578e4114ebc8c0f9fec","265ca39ad0ce090e790fc57e383ade73"}

    for i in w1_hash:
        asyncio.run(main(i))

# BaCk25
