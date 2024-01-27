from django.urls import path
from . import views

urlpatterns = [
    path("", views.comment, name="comment"),
    # path("<int:post_id>/", views.detail, name="detail"),
]