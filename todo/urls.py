from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path(route='login/', view=views.CustomLoginView.as_view(), name='login'),
    path(route='logout/', view=LogoutView.as_view(next_page='task-list'), name='logout'),
    path(route='signup/', view=views.RegisterView.as_view(), name='signup'),
    path(route='', view=views.TaskListView.as_view(), name='task-list'),
    path(route='create/', view=views.TaskCreateView.as_view(), name='task-create'),
    path(route='delete/<int:pk>/', view=views.TaskDeleteView.as_view(), name='task-delete'),
    path(route='clear/', view=views.TaskClearView.as_view(), name="task-clear"),
    path(route='status/<int:pk>/', view=views.TaskStatusView.as_view(), name='task-status'),
    path(route='update/<int:pk>/', view=views.TaskUpdateView.as_view(), name='task-update'),
]
