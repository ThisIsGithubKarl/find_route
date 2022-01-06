from django.core.exceptions import ValidationError
from django.db import models

from cities.models import City


class Train(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Номер поезда")
    from_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="from_city_set",
        verbose_name="Точка отправления"
    )
    to_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="to_city_set",
        verbose_name="Точка назначения"
    )
    travel_time = models.PositiveSmallIntegerField(verbose_name="Время в пути")

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError("Точка отправления и пункт назначения не должны совпадать")

        qs = Train.objects.filter(
            from_city=self.from_city,
            to_city=self.to_city,
            travel_time=self.travel_time
        ).exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError("Такой объект уже существует")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Поезд № {self.name} из {self.from_city} в {self.to_city}"

    class Meta:
        verbose_name = "Поезд"
        verbose_name_plural = "Поезда"
        ordering = ["from_city", "to_city"]
