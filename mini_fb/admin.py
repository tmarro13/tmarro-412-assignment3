from django.contrib import admin
from .models import Profile, Friend

# Register your models here.

from .models import *

admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Friend)
