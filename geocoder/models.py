from django.db import models
from django.utils import timezone


class Location(models.Model):
    address = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Адрес'
    )

    longitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Долгота'
    )

    latitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name='Широта'
    )

    request_data = models.DateTimeField(
        default=timezone.now(),
        verbose_name='Дата запроса',
        db_index=True
    )

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.address
