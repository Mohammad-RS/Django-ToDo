from django.db.models.base import Model as Model
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
from .forms import TaskForm

class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = "__all__"
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('task-list')


class RegisterView(FormView):
    template_name = 'todo/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('task-list'))  
        return super().get(*args, **kwargs)
    
    
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/index.html'
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'todo/index.html'
    context_object_name = 'tasks'
    ordering = '-id'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        search_q = self.request.GET.get('search_q', '')
        if search_q:
            context['tasks'] = context['tasks'].filter(Q(title__icontains=search_q) | Q(description__icontains=search_q))
        context['search_q'] = search_q
        return context


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    
    
class TaskStatusView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        obj = get_object_or_404(Task, pk=pk)
        obj.completed = not obj.completed
        obj.save()
        return redirect(reverse_lazy('task-list'))  
        
        
class TaskClearView(LoginRequiredMixin, View):
    def post(self, request):
        Task.objects.filter(completed=True).delete()
        return redirect(reverse_lazy('task-list'))  


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'todo/task-update.html'
    success_url = reverse_lazy('task-list')
    
    