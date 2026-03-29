from django.urls import path

from .views import (
    LegendDetailView,
    PatronLegendListView,
    ProvinceLegendListView,
    SeriesLegendListView,
    TagLegendListView,
)

urlpatterns = [
    path("legends/<slug:slug>/", LegendDetailView.as_view(), name="legend-detail"),
    path("series/<slug:slug>/", SeriesLegendListView.as_view(), name="legend-series-detail"),
    path("provinces/<slug:slug>/", ProvinceLegendListView.as_view(), name="legend-province-detail"),
    path("patrons/<slug:slug>/", PatronLegendListView.as_view(), name="legend-patron-detail"),
    path("tags/<slug:slug>/", TagLegendListView.as_view(), name="legend-tag-detail"),
]
