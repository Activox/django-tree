from django.core.exceptions import ValidationError
from django.db import models


class Tree(models.Model):
    value = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "deleted": self.deleted,
            "parent": self.parent.id if self.parent else None,
        }

    def clean(self):
        if self.parent and self.parent.children.count() >= 10:
            raise ValidationError("A parent node can have at most 10 children.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.value
