from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from habits.models import Habit
from habits.serializers import HabitSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class HabitViewSet(viewsets.ModelViewSet):
	queryset = Habit.objects.all()
	serializer_class = HabitSerializer
	
	def get_queryset(self):
		if self.action == 'public':
			return Habit.objects.filter(is_public=True)
		return Habit.objects.filter(user=self.request.user)
	
	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
	
	def get_permissions(self):
		if self.action in ['public', 'create']:
			self.permission_classes = [AllowAny]
		else:
			self.permission_classes = [IsAuthenticated]
		return [permission() for permission in self.permission_classes]
	
	@action(detail=False, methods=['get'], permission_classes=[AllowAny])
	def public(self, request):
		habits = Habit.objects.filter(is_public=True)
		page = self.paginate_queryset(habits)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(habits, many=True)
		return Response(serializer.data)