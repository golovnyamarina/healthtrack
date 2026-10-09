from django.db import models
from django.contrib.auth.models import User

class Measurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    upper_pressure = models.PositiveIntegerField(verbose_name='Верхнее давление')
    lower_pressure = models.PositiveIntegerField(verbose_name='Нижнее давление')
    pulse = models.PositiveIntegerField(verbose_name='Пульс')
    note = models.TextField(blank=True, verbose_name='Заметка')

    class Meta:
        ordering = ['-date']

    def is_high(self):
        return self.upper_pressure > 140 or self.lower_pressure > 90

    def __str__(self):
        return f'{self.user.username} - {self.date.strftime('%d.%m.%Y %H:%M')}'