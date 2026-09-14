from django.db import models


class Animal(models.Model):
    """A single animal shown on the site."""

    name = models.CharField(max_length=100, unique=True)
    emoji = models.CharField(
        max_length=10,
        blank=True,
        help_text="Emoji shown before the animal's name, e.g. 🦁",
    )
    image_url = models.URLField(
        max_length=500,
        help_text="Full URL of the card image.",
    )
    short_description = models.CharField(
        max_length=200,
        help_text="Short blurb shown on the card.",
    )
    full_description = models.TextField(
        help_text="Longer fact shown in the 'Learn More' popup.",
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Controls display order on the page (lower = first).",
    )

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name
