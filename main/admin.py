from django.contrib import admin
from main.models import ScoreAPILog, User

class LogAdmin(admin.ModelAdmin):
    list_display = ['user', 'score']
    list_editable = ['score']

# Register your models here.
admin.site.register(ScoreAPILog, LogAdmin)
admin.site.register(User)