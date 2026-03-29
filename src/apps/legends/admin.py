from django.contrib import admin, messages
from django.db.models import Prefetch
from django.utils import timezone

from .models import (
    Legend,
    LegendTranslation,
    Patron,
    PatronTranslation,
    Province,
    ProvinceTranslation,
    Series,
    SeriesTranslation,
    Tag,
    TagTranslation,
)


class LegendTranslationInline(admin.TabularInline):
    model = LegendTranslation
    extra = 0
    show_change_link = True
    fields = ("locale", "title", "slug", "is_published")
    prepopulated_fields = {"slug": ("title",)}


class BaseTaxonomyTranslationInline(admin.TabularInline):
    extra = 0
    show_change_link = True
    fields = ("locale", "name", "slug", "is_published")
    prepopulated_fields = {"slug": ("name",)}


class SeriesTranslationInline(BaseTaxonomyTranslationInline):
    model = SeriesTranslation


class ProvinceTranslationInline(BaseTaxonomyTranslationInline):
    model = ProvinceTranslation


class PatronTranslationInline(BaseTaxonomyTranslationInline):
    model = PatronTranslation


class TagTranslationInline(BaseTaxonomyTranslationInline):
    model = TagTranslation


class TranslatableCatalogAdmin(admin.ModelAdmin):
    list_display = ("id", "display_name", "available_locales", "updated_at")
    list_filter = ("translations__locale", "translations__is_published")
    search_fields = ("translations__name", "translations__slug", "translations__description")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related(
            Prefetch(
                "translations",
                queryset=self.translation_model.objects.order_by("locale"),
                to_attr="prefetched_translations",
            )
        )

    @admin.display(description="Name")
    def display_name(self, obj):
        return obj.display_name

    @admin.display(description="Locales")
    def available_locales(self, obj):
        return ", ".join(locale.upper() for locale in obj.available_locales) or "-"


class BaseTaxonomyTranslationAdmin(admin.ModelAdmin):
    list_display = ("name", "locale", "source_object", "is_published", "updated_at")
    list_filter = ("locale", "is_published")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    actions = ("publish_selected", "unpublish_selected")

    @admin.display(description="Object")
    def source_object(self, obj):
        return getattr(obj, self.source_field_name)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(self.source_field_name)

    @admin.action(description="Publish selected translations")
    def publish_selected(self, request, queryset):
        updated = queryset.update(is_published=True, updated_at=timezone.now())
        self.message_user(request, f"Published {updated} translations.", level=messages.SUCCESS)

    @admin.action(description="Unpublish selected translations")
    def unpublish_selected(self, request, queryset):
        updated = queryset.update(is_published=False, updated_at=timezone.now())
        self.message_user(request, f"Unpublished {updated} translations.", level=messages.SUCCESS)


@admin.register(Series)
class SeriesAdmin(TranslatableCatalogAdmin):
    inlines = (SeriesTranslationInline,)
    translation_model = SeriesTranslation


@admin.register(Province)
class ProvinceAdmin(TranslatableCatalogAdmin):
    inlines = (ProvinceTranslationInline,)
    translation_model = ProvinceTranslation


@admin.register(Patron)
class PatronAdmin(TranslatableCatalogAdmin):
    inlines = (PatronTranslationInline,)
    translation_model = PatronTranslation


@admin.register(Tag)
class TagAdmin(TranslatableCatalogAdmin):
    inlines = (TagTranslationInline,)
    translation_model = TagTranslation


@admin.register(SeriesTranslation)
class SeriesTranslationAdmin(BaseTaxonomyTranslationAdmin):
    autocomplete_fields = ("series",)
    source_field_name = "series"


@admin.register(ProvinceTranslation)
class ProvinceTranslationAdmin(BaseTaxonomyTranslationAdmin):
    autocomplete_fields = ("province",)
    source_field_name = "province"


@admin.register(PatronTranslation)
class PatronTranslationAdmin(BaseTaxonomyTranslationAdmin):
    autocomplete_fields = ("patron",)
    source_field_name = "patron"


@admin.register(TagTranslation)
class TagTranslationAdmin(BaseTaxonomyTranslationAdmin):
    autocomplete_fields = ("tag",)
    source_field_name = "tag"


@admin.register(Legend)
class LegendAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "display_title",
        "status",
        "published_at",
        "series",
        "province",
        "patron",
        "created_at",
    )
    list_filter = (
        "status",
        "series",
        "province",
        "patron",
        "translations__locale",
        "series__translations__locale",
        "province__translations__locale",
        "patron__translations__locale",
        "tags__translations__locale",
    )
    search_fields = ("translations__title", "translations__slug")
    filter_horizontal = ("tags",)
    inlines = (LegendTranslationInline,)
    actions = ("publish_selected", "unpublish_selected")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("series", "province", "patron").prefetch_related(
            "translations",
            "series__translations",
            "province__translations",
            "patron__translations",
        )

    @admin.display(description="Title")
    def display_title(self, obj):
        return obj.display_title

    @admin.action(description="Publish selected legends")
    def publish_selected(self, request, queryset):
        updated = 0
        for legend in queryset:
            if legend.status != Legend.Status.PUBLISHED:
                legend.status = Legend.Status.PUBLISHED
                if legend.published_at is None:
                    legend.published_at = timezone.now()
                legend.save(update_fields=["status", "published_at", "updated_at"])
                updated += 1
        self.message_user(request, f"Published {updated} legends.", level=messages.SUCCESS)

    @admin.action(description="Unpublish selected legends")
    def unpublish_selected(self, request, queryset):
        updated = queryset.update(
            status=Legend.Status.DRAFT,
            published_at=None,
            updated_at=timezone.now(),
        )
        self.message_user(request, f"Unpublished {updated} legends.", level=messages.SUCCESS)


@admin.register(LegendTranslation)
class LegendTranslationAdmin(admin.ModelAdmin):
    list_display = ("title", "locale", "legend", "legend_status", "is_published", "updated_at")
    list_filter = ("locale", "is_published", "legend__status")
    search_fields = ("title", "slug", "legend__translations__title")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("legend",)
    actions = ("publish_selected", "unpublish_selected")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("legend")

    @admin.display(description="Legend status")
    def legend_status(self, obj):
        return obj.legend.status

    @admin.action(description="Publish selected translations")
    def publish_selected(self, request, queryset):
        updated = queryset.update(is_published=True, updated_at=timezone.now())
        self.message_user(request, f"Published {updated} translations.", level=messages.SUCCESS)

    @admin.action(description="Unpublish selected translations")
    def unpublish_selected(self, request, queryset):
        updated = queryset.update(is_published=False, updated_at=timezone.now())
        self.message_user(request, f"Unpublished {updated} translations.", level=messages.SUCCESS)
