from rest_framework.serializers import ValidationError


def validate_related_habit_or_reward(value, related_habit, reward):
    """Исключить одновременный выбор связанной привычки и вознаграждения"""
    if related_habit and reward:
        raise ValidationError('Нельзя одновременно указать связанную привычку и вознаграждение. Выберите что-то одно.')


def validate_duration(value):
    """Время выполнения не больше 120 секунд"""
    if value > 120:
        raise ValidationError('Время выполнения не должно превышать 120 секунд.')


def validate_related_habit(value):
    """В связанные привычки могут попадать только приятные привычки"""
    if value and not value.is_pleasant:
        raise ValidationError('Связанная привычка должна быть приятной.')


def validate_pleasant_habit(value, related_habit, reward):
    """У приятной привычки не может быть вознаграждения или связанной привычки"""
    if value:
        if related_habit:
            raise ValidationError('У приятной привычки не может быть связанной привычки.')
        if reward:
            raise ValidationError('У приятной привычки не может быть вознаграждения.')


def validate_period(value):
    """Периодичность от 1 до 7 дней"""
    if value < 1 or value > 7:
        raise ValidationError('Периодичность должна быть от 1 до 7 дней.')