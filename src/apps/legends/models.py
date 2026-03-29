from django.db import models
from django.urls import reverse
from django.utils import timezone, translation

from apps.core.models import TimeStampedModel


class ContentLocale(models.TextChoices):
    RU = "ru", "Russian"
    EN = "en", "English"
    DE = "de", "German"
    ES = "es", "Spanish"


def get_active_locale() -> str:
    language_code = (translation.get_language() or ContentLocale.RU).split("-")[0]
    supported_languages = {code for code, _label in ContentLocale.choices}
    if language_code not in supported_languages:
        return ContentLocale.RU
    return language_code


class TranslatableCatalogModel(TimeStampedModel):
    class Meta:
        abstract = True
        ordering = ("id",)

    def _get_translation_candidates(self, *, published_only: bool = False):
        translations = getattr(self, "published_translations", None)
        if translations is None:
            translations = getattr(self, "prefetched_translations", None)
        if translations is None:
            queryset = self.translations.all()
            if published_only:
                queryset = queryset.filter(is_published=True)
            translations = list(queryset)
        if published_only:
            translations = [item for item in translations if item.is_published]
        return translations

    def get_translation(self, locale: str | None = None, *, published_only: bool = False):
        locale = locale or get_active_locale()
        translations = self._get_translation_candidates(published_only=published_only)
        if not translations:
            return None

        for target_locale in (locale, ContentLocale.RU):
            for item in translations:
                if item.locale == target_locale:
                    return item

        return translations[0]

    @property
    def display_name(self) -> str:
        item = self.get_translation()
        if item is not None:
            return item.name
        return f"{self._meta.verbose_name.title()} #{self.pk}"

    @property
    def display_description(self) -> str:
        item = self.get_translation()
        return item.description if item is not None else ""

    @property
    def available_locales(self) -> list[str]:
        return [item.locale for item in self._get_translation_candidates()]

    def __str__(self) -> str:
        return self.display_name

    def get_absolute_url(self) -> str:
        item = self.get_translation(published_only=True)
        if item is None:
            return "#"
        return item.get_absolute_url()


class TaxonomyTranslationModel(TimeStampedModel):
    locale = models.CharField(max_length=2, choices=ContentLocale.choices)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True, db_index=True)

    url_name: str | None = None
    source_field_name: str | None = None

    class Meta:
        abstract = True
        ordering = ("locale", "name")
        indexes = [
            models.Index(fields=("locale", "slug")),
            models.Index(fields=("is_published", "locale")),
        ]

    def __str__(self) -> str:
        return f"{self.name} [{self.locale}]"

    def get_source_object(self):
        if not self.source_field_name:
            raise AttributeError("source_field_name is not configured.")
        return getattr(self, self.source_field_name)

    def get_sibling_translation(self, locale: str, *, published_only: bool = True):
        return self.get_source_object().get_translation(
            locale=locale,
            published_only=published_only,
        )

    def get_absolute_url(self) -> str:
        if self.url_name is None:
            return "#"
        with translation.override(self.locale):
            return reverse(self.url_name, kwargs={"slug": self.slug})


class Series(TranslatableCatalogModel):
    pass


class Province(TranslatableCatalogModel):
    pass


class Patron(TranslatableCatalogModel):
    pass


class Tag(TranslatableCatalogModel):
    pass


class SeriesTranslation(TaxonomyTranslationModel):
    url_name = "legend-series-detail"
    source_field_name = "series"

    series = models.ForeignKey(
        Series,
        on_delete=models.CASCADE,
        related_name="translations",
    )

    class Meta(TaxonomyTranslationModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("series", "locale"),
                name="unique_series_translation_per_locale",
            ),
            models.UniqueConstraint(
                fields=("locale", "slug"),
                name="unique_series_translation_slug_per_locale",
            ),
        ]


class ProvinceTranslation(TaxonomyTranslationModel):
    url_name = "legend-province-detail"
    source_field_name = "province"

    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name="translations",
    )

    class Meta(TaxonomyTranslationModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("province", "locale"),
                name="unique_province_translation_per_locale",
            ),
            models.UniqueConstraint(
                fields=("locale", "slug"),
                name="unique_province_translation_slug_per_locale",
            ),
        ]


class PatronTranslation(TaxonomyTranslationModel):
    url_name = "legend-patron-detail"
    source_field_name = "patron"

    patron = models.ForeignKey(
        Patron,
        on_delete=models.CASCADE,
        related_name="translations",
    )

    class Meta(TaxonomyTranslationModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("patron", "locale"),
                name="unique_patron_translation_per_locale",
            ),
            models.UniqueConstraint(
                fields=("locale", "slug"),
                name="unique_patron_translation_slug_per_locale",
            ),
        ]


class TagTranslation(TaxonomyTranslationModel):
    url_name = "legend-tag-detail"
    source_field_name = "tag"

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name="translations",
    )

    class Meta(TaxonomyTranslationModel.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=("tag", "locale"),
                name="unique_tag_translation_per_locale",
            ),
            models.UniqueConstraint(
                fields=("locale", "slug"),
                name="unique_tag_translation_slug_per_locale",
            ),
        ]


class Legend(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.DRAFT,
        db_index=True,
    )
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    hero_image = models.ImageField(upload_to="legends/hero-images/", null=True, blank=True)
    series = models.ForeignKey(
        Series,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="legends",
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="legends",
    )
    patron = models.ForeignKey(
        Patron,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="legends",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="legends")

    class Meta:
        ordering = ("-published_at", "-created_at")

    def __str__(self) -> str:
        return self.display_title

    @property
    def display_title(self) -> str:
        preferred = self.get_translation(locale=ContentLocale.RU)
        if preferred:
            return preferred.title
        first_translation = self.get_translation()
        if first_translation:
            return first_translation.title
        return f"Legend #{self.pk}"

    def get_translation(self, locale: str | None = None, *, published_only: bool = False):
        locale = locale or get_active_locale()
        queryset = self.translations.all()
        if published_only:
            queryset = queryset.filter(is_published=True)

        item = queryset.filter(locale=locale).first()
        if item is not None:
            return item

        fallback = queryset.filter(locale=ContentLocale.RU).first()
        if fallback is not None:
            return fallback

        return queryset.first()

    def publish(self) -> None:
        self.status = self.Status.PUBLISHED
        if self.published_at is None:
            self.published_at = timezone.now()
        self.save(update_fields=["status", "published_at", "updated_at"])

    def unpublish(self) -> None:
        self.status = self.Status.DRAFT
        self.published_at = None
        self.save(update_fields=["status", "published_at", "updated_at"])


class LegendTranslation(TimeStampedModel):
    legend = models.ForeignKey(
        Legend,
        on_delete=models.CASCADE,
        related_name="translations",
    )
    locale = models.CharField(max_length=2, choices=ContentLocale.choices)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=320, blank=True)
    is_published = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ("locale", "title")
        constraints = [
            models.UniqueConstraint(
                fields=("legend", "locale"),
                name="unique_legend_translation_per_locale",
            ),
            models.UniqueConstraint(
                fields=("locale", "slug"),
                name="unique_translation_slug_per_locale",
            ),
        ]
        indexes = [
            models.Index(fields=("locale", "slug")),
            models.Index(fields=("is_published", "locale")),
        ]

    def __str__(self) -> str:
        return f"{self.title} [{self.locale}]"

    def get_absolute_url(self) -> str:
        with translation.override(self.locale):
            return reverse("legend-detail", kwargs={"slug": self.slug})
