from django.contrib import admin

# Register your models here.
from .models import Examset,Question,Marks



admin.site.register(Examset)
admin.site.register(Question)
admin.site.register(Marks)

