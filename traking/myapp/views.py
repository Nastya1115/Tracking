from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from myapp.models import *
from django.contrib import messages
from myapp.forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from myapp.mixins import *


# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserForm()

    return render(
        request,
        template_name = 'register.html',
        context = {'form': form}
    )

def login_user(request):
    if request.method == 'POST':
        form = UserAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
            else:
                messages.error(request, 'invalid login or password')
    else:
        form = UserAuthForm()

    return render(
        request,
        template_name = 'login.html',
        context = {'form': form}
    )

def logout_user(request):
    logout(request)
    return redirect('task_list')

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.creator = self.request.user  # Привязываем текущего пользователя к полю creator
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'update_task.html'
    success_url = '/'

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = 'delete_task.html'
    success_url = '/'

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'

    def get_queryset(self):
        return Task.objects.all().order_by('priority')