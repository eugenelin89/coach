from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GamePlayViewSet, RecommendationView

router = DefaultRouter()
router.register('plays', GamePlayViewSet, basename='plays')

urlpatterns = [
    path('', include(router.urls)),
    path('recommendations/', RecommendationView.as_view(), name='recommendation'),
]
