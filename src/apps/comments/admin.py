from django.contrib import admin, messages

from .models import Comment, CommentModerationEvent


class CommentModerationEventInline(admin.TabularInline):
    model = CommentModerationEvent
    extra = 0
    can_delete = False
    fields = ("created_at", "actor", "from_status", "to_status", "note")
    readonly_fields = fields


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "author_name",
        "legend_translation",
        "translation_locale",
        "status",
        "created_at",
        "moderated_at",
    )
    list_filter = ("status", "legend_translation__locale", "created_at")
    search_fields = (
        "author_name",
        "author_email",
        "body",
        "legend_translation__title",
        "legend_translation__slug",
    )
    autocomplete_fields = ("legend_translation",)
    readonly_fields = ("created_at", "moderated_at")
    list_select_related = ("legend_translation",)
    inlines = (CommentModerationEventInline,)
    actions = ("approve_selected", "reject_selected", "mark_as_spam")

    @admin.display(description="Locale")
    def translation_locale(self, obj):
        return obj.legend_translation.locale

    def _moderate_queryset(self, request, queryset, target_status, note):
        updated = 0
        for comment in queryset.select_related("legend_translation"):
            changed = comment.moderate(
                to_status=target_status,
                moderator=request.user,
                note=note,
            )
            if changed:
                updated += 1
        self.message_user(
            request,
            f"Updated {updated} comments to '{target_status}'.",
            level=messages.SUCCESS,
        )

    @admin.action(description="Approve selected comments")
    def approve_selected(self, request, queryset):
        self._moderate_queryset(
            request,
            queryset,
            Comment.Status.APPROVED,
            "Approved in Django admin.",
        )

    @admin.action(description="Reject selected comments")
    def reject_selected(self, request, queryset):
        self._moderate_queryset(
            request,
            queryset,
            Comment.Status.REJECTED,
            "Rejected in Django admin.",
        )

    @admin.action(description="Mark selected comments as spam")
    def mark_as_spam(self, request, queryset):
        self._moderate_queryset(
            request,
            queryset,
            Comment.Status.SPAM,
            "Marked as spam in Django admin.",
        )


@admin.register(CommentModerationEvent)
class CommentModerationEventAdmin(admin.ModelAdmin):
    list_display = ("comment", "actor", "from_status", "to_status", "created_at")
    list_filter = ("from_status", "to_status", "created_at")
    search_fields = ("comment__author_name", "actor__username", "note")
    readonly_fields = ("comment", "actor", "from_status", "to_status", "note", "created_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
