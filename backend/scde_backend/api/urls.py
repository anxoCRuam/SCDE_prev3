from django.urls import path
from api.views import EntityView


urlpatterns = [
    path("<str:entidad>/", EntityView.as_view()),
    path("<str:entidad>/<str:pk>/", EntityView.as_view()),
]
