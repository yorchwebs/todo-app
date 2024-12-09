from django.contrib import admin

# Register your models here.
from .models import List, Task

admin.site.register(List)
admin.site.register(Task)