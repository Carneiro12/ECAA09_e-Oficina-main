from django.urls import path
from banco import views

urlpatterns = [
    path("", views.servico_index, name="servico_index"),
    path("<int:servico_id>/", views.servico_detail, name="servico_detail"),
]