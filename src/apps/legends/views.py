from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from apps.comments.forms import CommentForm
from apps.comments.models import Comment

from .models import (
    LegendTranslation,
    PatronTranslation,
    ProvinceTranslation,
    SeriesTranslation,
    TagTranslation,
)
from .public import (
    get_current_locale,
    get_published_taxonomy_translation,
    get_published_translations,
)


class LegendDetailView(DetailView):
    template_name = "legends/detail.html"
    context_object_name = "translation"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    form_class = CommentForm
    show_all_comments_param = "show_all_comments"

    def get_queryset(self):
        return get_published_translations()

    def should_show_all_comments(self) -> bool:
        source = self.request.POST if self.request.method == "POST" else self.request.GET
        return source.get(self.show_all_comments_param) in {"1", "true", "on", "yes"}

    def get_form(self):
        if self.request.method == "POST":
            return self.form_class(self.request.POST)
        return self.form_class()

    def get_approved_comments_queryset(self):
        queryset = Comment.objects.filter(
            status=Comment.Status.APPROVED,
            legend_translation__is_published=True,
        ).select_related("legend_translation")

        if self.should_show_all_comments():
            queryset = queryset.filter(legend_translation__legend=self.object.legend)
        else:
            queryset = queryset.filter(legend_translation=self.object)

        return queryset.order_by("created_at")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.legend_translation = self.object
            comment.status = Comment.Status.PENDING
            comment.save()
            messages.success(
                request,
                _(
                    "Комментарий отправлен на модерацию. Он появится после проверки редактором."
                ),
            )
            redirect_url = self.object.get_absolute_url()
            if self.should_show_all_comments():
                redirect_url = f"{redirect_url}?{self.show_all_comments_param}=1"
            return redirect(f"{redirect_url}#comments")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["alternate_translations"] = (
            self.object.legend.translations.filter(is_published=True).order_by("locale")
        )
        context["approved_comments"] = self.get_approved_comments_queryset()
        context["comment_form"] = kwargs.get("form", self.get_form())
        context["show_all_comments"] = self.should_show_all_comments()
        return context


class BaseTaxonomyLegendListView(ListView):
    template_name = "legends/taxonomy_list.html"
    context_object_name = "legends"
    taxonomy_translation_model = None
    taxonomy_filter_field = ""
    taxonomy_label = _("Раздел")

    def dispatch(self, request, *args, **kwargs):
        self.taxonomy_object = self.get_taxonomy_object()
        return super().dispatch(request, *args, **kwargs)

    def get_taxonomy_object(self):
        if self.taxonomy_translation_model is None:
            raise Http404("Taxonomy translation model is not configured.")

        taxonomy_translation = get_published_taxonomy_translation(
            self.taxonomy_translation_model,
            slug=self.kwargs["slug"],
            locale=get_current_locale(),
        )
        if taxonomy_translation is None:
            raise Http404("Published taxonomy translation was not found.")
        return taxonomy_translation

    def get_queryset(self):
        queryset = get_published_translations(locale=get_current_locale())
        return queryset.filter(
            **{self.taxonomy_filter_field: self.taxonomy_object.get_source_object()}
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["taxonomy_object"] = self.taxonomy_object
        context["taxonomy_label"] = self.taxonomy_label
        return context


class SeriesLegendListView(BaseTaxonomyLegendListView):
    taxonomy_translation_model = SeriesTranslation
    taxonomy_filter_field = "legend__series"
    taxonomy_label = _("Серия")


class ProvinceLegendListView(BaseTaxonomyLegendListView):
    taxonomy_translation_model = ProvinceTranslation
    taxonomy_filter_field = "legend__province"
    taxonomy_label = _("Провинция")


class PatronLegendListView(BaseTaxonomyLegendListView):
    taxonomy_translation_model = PatronTranslation
    taxonomy_filter_field = "legend__patron"
    taxonomy_label = _("Покровитель")


class TagLegendListView(BaseTaxonomyLegendListView):
    taxonomy_translation_model = TagTranslation
    taxonomy_filter_field = "legend__tags"
    taxonomy_label = _("Тег")
