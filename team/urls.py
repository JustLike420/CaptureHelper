from django.urls import path

from . import views

teams = views.TeamViewSet.as_view({
    'get': 'list',
    # 'post': 'create'
})

detail_teams = views.TeamViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    # 'delete': 'destroy'
})

urlpatterns = [
    path('', teams, name='teams'),
    path('<int:pk>/', detail_teams, name='detail_teams'),
]
