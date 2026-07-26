import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from habits.models import Habit


@shared_task
def send_telegram_reminder(habit_id, chat_id):
	"""Отправляет одно напоминание в Telegram"""
	habit = Habit.objects.get(pk=habit_id)
	bot_token = settings.TELEGRAM_BOT_TOKEN
	message = f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
	url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
	
	response = requests.post(url, data={'chat_id': chat_id, 'text': message})
	if response.status_code != 200:
		print(f"Ошибка отправки в Telegram: {response.text}")


@shared_task
def send_habit_reminders():
	"""Периодическая задача: рассылает напоминания о привычках"""
	now = timezone.now()
	habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)
	habits = habits.exclude(user__telegram_chat_id__isnull=True)
	
	for habit_id, chat_id in habits.values_list('pk', 'user__telegram_chat_id'):
		send_telegram_reminder.delay(habit_id, chat_id)