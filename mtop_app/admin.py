from django.contrib import admin
from .models import Plan, Question, ContactRequest
# Register your models here.
admin.site.register(Plan)
admin.site.register(Question)
admin.site.register(ContactRequest)
