import random
import string


def generate_random_string(length=10):
    """Генерирует случайную строку из букв и цифр."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


def generate_random_email(domain="example.com"):
    """Генерирует случайный email."""
    return f"{generate_random_string(8)}@{domain}"


def generate_random_phone():
    """Генерирует случайный номер телефона (пример для РФ)."""
    return f"+79{random.randint(100000000, 999999999)}"
