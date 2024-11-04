from django.contrib import admin
from myapp.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Task)