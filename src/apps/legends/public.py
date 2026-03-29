from django.conf import settings
from django.db.models import Prefetch
from django.utils.translation import get_language

from .models import (
    ContentLocale,
    Legend,
    LegendTranslation,
    PatronTranslation,
    ProvinceTranslation,
    SeriesTranslation,
    TagTranslation,
)


def get_current_locale() -> str:
    language_code = (get_language() or settings.LANGUAGE_CODE).split("-")[0]
    supported_languages = {code for code, _label in settings.LANGUAGES}
    if language_code not in supported_languages:
        return settings.LANGUAGE_CODE
    return language_code


def build_taxonomy_translation_prefetch(path: str, model, source_field_name: str):
    return Prefetch(
        path,
        queryset=model.objects.filter(is_published=True)
        .only(
            "id",
            f"{source_field_name}_id",
            "locale",
            "name",
            "slug",
            "description",
            "is_published",
        )
        .order_by("locale"),
        to_attr="published_translations",
    )


def get_published_translations(locale: str | None = None):
    locale = locale or get_current_locale()
    return (
        LegendTranslation.objects.filter(
            locale=locale,
            is_published=True,
            legend__status=Legend.Status.PUBLISHED,
        )
        .select_related(
            "legend",
            "legend__series",
            "legend__province",
            "legend__patron",
        )
        .prefetch_related(
            "legend__tags",
            Prefetch(
                "legend__translations",
                queryset=LegendTranslation.objects.filter(is_published=True)
                .only("id", "legend_id", "locale", "slug", "title", "is_published")
                .order_by("locale"),
                to_attr="published_translations",
            ),
            build_taxonomy_translation_prefetch(
                "legend__series__translations",
                SeriesTranslation,
                "series",
            ),
            build_taxonomy_translation_prefetch(
                "legend__province__translations",
                ProvinceTranslation,
                "province",
            ),
            build_taxonomy_translation_prefetch(
                "legend__patron__translations",
                PatronTranslation,
                "patron",
            ),
            build_taxonomy_translation_prefetch(
                "legend__tags__translations",
                TagTranslation,
                "tag",
            ),
        )
        .order_by("-legend__published_at", "-legend__created_at")
    )


def get_published_taxonomy_translation(model, slug: str, locale: str):
    return (
        model.objects.filter(locale=locale, slug=slug, is_published=True)
        .select_related(model.source_field_name)
        .first()
    )
