import re
from django.core.exceptions import ValidationError

def youtube_link_validator(value):
    """
    Валидатор, который разрешает только ссылки на YouTube.
    """
    youtube_pattern = re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/")
    if not youtube_pattern.match(value):
        raise ValidationError("Разрешены только ссылки на YouTube.")
