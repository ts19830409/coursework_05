from django.db import models
from django.conf import settings


class Habit(models.Model):
	PERIOD_CHOICES = [(i, f'{i} день/дня/дней') for i in range(1, 8)]
	
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits',
	                         verbose_name='Пользователь')
	place = models.CharField(max_length=200, verbose_name='Место')
	time = models.TimeField(verbose_name='Время')
	action = models.CharField(max_length=200, verbose_name='Действие')
	is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
	related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
	                                  related_name='related_to', verbose_name='Связанная привычка')
	period = models.PositiveSmallIntegerField(default=1, choices=PERIOD_CHOICES, verbose_name='Периодичность (дней)')
	reward = models.CharField(max_length=200, null=True, blank=True, verbose_name='Вознаграждение')
	duration = models.PositiveSmallIntegerField(default=60, verbose_name='Время на выполнение (секунд)')
	is_public = models.BooleanField(default=False, verbose_name='Публичная')
	
	class Meta:
		verbose_name = 'Привычка'
		verbose_name_plural = 'Привычки'
	
	def __str__(self):
		return f'{self.action} в {self.place} в {self.time}'