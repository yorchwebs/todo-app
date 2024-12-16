from django.urls import path
from . import views


app_name = "todo"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("list/<int:list_id>/", views.create_task, name="create_task"),
    path("list/<int:list_id>/update/", views.update_list, name="update_list"),
    path("list/<int:list_id>/delete/", views.delete_list, name="delete_list"),
    path("list/<int:list_id>/task/<int:task_id>/update/", views.update_task, name="update_task"),
    path("list/<int:list_id>/task/<int:task_id>/delete/", views.delete_task, name="delete_task"),
]
