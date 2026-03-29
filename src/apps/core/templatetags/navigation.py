from django import template
from django.urls import reverse
from django.utils import translation

register = template.Library()

TAXONOMY_VIEW_NAMES = {
    "legend-series-detail",
    "legend-province-detail",
    "legend-patron-detail",
    "legend-tag-detail",
}

PRESERVED_QUERY_KEYS = {"show_all_comments"}


def append_preserved_query(url: str, request) -> str:
    preserved_items = []
    for key in PRESERVED_QUERY_KEYS:
        value = request.GET.get(key)
        if value:
            preserved_items.append(f"{key}={value}")

    if not preserved_items:
        return url

    separator = "&" if "?" in url else "?"
    return f"{url}{separator}{'&'.join(preserved_items)}"


@register.simple_tag(takes_context=True)
def switch_language_url(context, language_code: str) -> str:
    request = context.get("request")
    if request is None:
        return "/"

    with translation.override(language_code):
        fallback_url = reverse("home")

    resolver_match = getattr(request, "resolver_match", None)
    if resolver_match is None:
        return fallback_url

    view_name = resolver_match.view_name

    if view_name == "home":
        return append_preserved_query(fallback_url, request)

    if view_name == "legend-detail":
        current_translation = context.get("translation")
        if current_translation is not None:
            target_translation = current_translation.legend.get_translation(
                locale=language_code,
                published_only=True,
            )
            if target_translation is not None:
                return append_preserved_query(target_translation.get_absolute_url(), request)
        return append_preserved_query(fallback_url, request)

    if view_name in TAXONOMY_VIEW_NAMES:
        taxonomy_object = context.get("taxonomy_object")
        if taxonomy_object is not None and hasattr(taxonomy_object, "get_sibling_translation"):
            target_translation = taxonomy_object.get_sibling_translation(
                language_code,
                published_only=True,
            )
            if target_translation is not None:
                return append_preserved_query(target_translation.get_absolute_url(), request)
        return append_preserved_query(fallback_url, request)

    return append_preserved_query(fallback_url, request)
