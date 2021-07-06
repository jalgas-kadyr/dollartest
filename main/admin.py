from django.contrib import admin
from main import models

admin.site.register(models.Interval)
admin.site.register(models.Check)
admin.site.register(models.Config)
admin.site.register(models.Change)
