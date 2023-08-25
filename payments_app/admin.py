from django.contrib import admin

# Register your models here.
from .models import Invoice, Wallet
admin.site.register(Invoice),
admin.site.register(Wallet),

