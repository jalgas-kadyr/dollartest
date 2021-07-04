from django.contrib import admin
from main import models

admin.site.register(models.Result)
admin.site.register(models.Config)
admin.site.register(models.Change)
