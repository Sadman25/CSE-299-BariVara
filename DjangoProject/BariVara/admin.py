from django.contrib import admin
from .models import advertisements,images,Comment
# Register your models here.
admin.site.register(advertisements)
admin.site.register(images)
admin.site.register(Comment)