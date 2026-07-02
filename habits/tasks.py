import requests
from celery import shared_task
from django.conf import settings
from habits.models import Habit


@shared_task
def send_telegram_reminder(habit_id, chat_id):
	"""Отправляет напоминание о привычке в Telegram"""
	habit = Habit.objects.get(pk=habit_id)
	bot_token = settings.TELEGRAM_BOT_TOKEN
	
	message = f"Напоминание: {habit.action} в {habit.place} в {habit.time}"
	url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
	
	requests.post(url, data={
		'chat_id': chat_id,
		'text': message,
	})