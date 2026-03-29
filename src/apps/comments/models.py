from django.conf import settings
from django.db import models
from django.utils import timezone

from .validators import validate_plain_text


class Comment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        SPAM = "spam", "Spam"

    legend_translation = models.ForeignKey(
        "legends.LegendTranslation",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author_name = models.CharField(max_length=120)
    author_email = models.EmailField(blank=True, null=True)
    body = models.TextField(validators=[validate_plain_text])
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    moderated_at = models.DateTimeField(null=True, blank=True)
    moderator_note = models.TextField(blank=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=("status", "created_at"))]

    def __str__(self) -> str:
        return f"{self.author_name} on {self.legend_translation}"

    def moderate(self, *, to_status: str, moderator=None, note: str = "") -> bool:
        previous_status = self.status
        if previous_status == to_status and note == self.moderator_note:
            return False
        self.status = to_status
        self.moderated_at = timezone.now()
        self.moderator_note = note
        self.save(update_fields=["status", "moderated_at", "moderator_note"])
        CommentModerationEvent.objects.create(
            comment=self,
            actor=moderator,
            from_status=previous_status,
            to_status=to_status,
            note=note,
        )
        return True


class CommentModerationEvent(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="moderation_events",
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comment_moderation_events",
    )
    from_status = models.CharField(max_length=16, choices=Comment.Status.choices)
    to_status = models.CharField(max_length=16, choices=Comment.Status.choices)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.comment_id}: {self.from_status} -> {self.to_status}"
