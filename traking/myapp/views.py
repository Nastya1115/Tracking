from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
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
        form.instance.creator = self.request.user
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
        option = self.request.GET.get('option')
        if option:
            return Task.objects.all().order_by(option)
        else:
            return Task.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['options'] = ['priority', 'title', 'status']
        context['selected_option'] = self.request.GET.get('option')
        return context
    
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_object().comments.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        form.instance.author = self.request.user
        form.instance.task = self.get_object()
        
        if form.is_valid():
            form.save()
            return redirect('detail_task', pk = self.get_object().id)
        