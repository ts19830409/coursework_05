from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from habits.models import Habit


class HabitTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(email='test@test.ru', password='test123')
		self.client.force_authenticate(user=self.user)
		self.habit_data = {
			'place': 'Дом',
			'time': '08:00:00',
			'action': 'Зарядка',
			'period': 1,
			'duration': 60,
		}
	
	def test_create_habit(self):
		response = self.client.post('/api/habits/', self.habit_data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	
	def test_get_my_habits(self):
		Habit.objects.create(user=self.user, **self.habit_data)
		response = self.client.get('/api/habits/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data['results']), 1)
	
	def test_public_habits(self):
		Habit.objects.create(user=self.user, is_public=True, **self.habit_data)
		response = self.client.get('/api/habits/public/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_related_and_reward_validation(self):
		data = {**self.habit_data, 'reward': 'Шоколадка', 'related_habit': 1}
		response = self.client.post('/api/habits/', data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_duration_validation(self):
		data = {**self.habit_data, 'duration': 200}
		response = self.client.post('/api/habits/', data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_period_validation(self):
		data = {**self.habit_data, 'period': 10}
		response = self.client.post('/api/habits/', data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)