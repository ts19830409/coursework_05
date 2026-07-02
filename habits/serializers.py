from rest_framework import serializers
from habits.models import Habit
from habits.validators import (
	validate_related_habit_or_reward,
	validate_duration,
	validate_related_habit,
	validate_pleasant_habit,
	validate_period,
)


class HabitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Habit
		fields = '__all__'
		read_only_fields = ['user']
	
	def validate(self, data):
		related_habit = data.get('related_habit')
		reward = data.get('reward')
		is_pleasant = data.get('is_pleasant')
		duration = data.get('duration')
		period = data.get('period')
		
		validate_related_habit_or_reward(None, related_habit, reward)
		validate_duration(duration)
		if related_habit:
			validate_related_habit(related_habit)
		validate_pleasant_habit(is_pleasant, related_habit, reward)
		validate_period(period)
		
		return data