from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .serializers import TeamSerializer
from .models import Team


class PaginationTeam(PageNumberPagination):
    page_size = 5
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class TeamViewSet(viewsets.ModelViewSet):
    """Посмотреть/создать команду CRUD"""
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    pagination_class = PaginationTeam
