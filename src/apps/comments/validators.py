from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


def validate_plain_text(value: str) -> None:
    if strip_tags(value) != value:
        raise ValidationError("HTML is not allowed in comments.")

