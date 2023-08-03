from django.db import models


class Tree(models.Model):
    value = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.value
