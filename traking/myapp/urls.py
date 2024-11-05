from django.urls import path
import myapp.views as views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("create_task/", views.TaskCreateView.as_view(), name="create_task"),
    path("update_task/<int:pk>/", views.TaskUpdateView.as_view(), name="update_task"),
    path("delete_task/<int:pk>/", views.TaskDeleteView.as_view(), name="delete_task"),
    path("detail_task/<int:pk>/", views.TaskDetailView.as_view(), name="detail_task"),
]