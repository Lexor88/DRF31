# courses/validators.py
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

def validate_link(value):
    """Валидатор для проверки ссылок на сторонние ресурсы."""
    allowed_domain = "youtube.com"
    parsed_url = urlparse(value)
    if parsed_url.netloc and allowed_domain not in parsed_url.netloc:
        raise ValidationError("Ссылки на сторонние ресурсы запрещены, кроме youtube.com.")
