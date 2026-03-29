from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("author_name", "author_email", "body")
        labels = {
            "author_name": _("Имя"),
            "author_email": _("Email"),
            "body": _("Текст комментария"),
        }
        widgets = {
            "author_name": forms.TextInput(
                attrs={
                    "autocomplete": "name",
                    "maxlength": "120",
                }
            ),
            "author_email": forms.EmailInput(
                attrs={
                    "autocomplete": "email",
                    "maxlength": "254",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "rows": 6,
                }
            ),
        }

    def clean_author_name(self):
        value = (self.cleaned_data.get("author_name") or "").strip()
        if not value:
            raise forms.ValidationError(_("Введите имя."))
        return value

    def clean_author_email(self):
        value = self.cleaned_data.get("author_email")
        if value:
            return value.strip()
        return None

    def clean_body(self):
        value = (self.cleaned_data.get("body") or "").strip()
        if not value:
            raise forms.ValidationError(_("Введите текст комментария."))
        return value

