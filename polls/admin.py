from django.contrib import admin

# Register your models here.
from . models import Poll,choice

admin.site.register(choice)
admin.site.register(Poll)
