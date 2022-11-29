from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TeamSerializer
from .models import Team


class TeamViewSet(viewsets.ModelViewSet):
    """Посмотреть/создать команду CRUD"""
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
