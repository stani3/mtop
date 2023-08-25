from django.contrib import admin

# Register your models here.
from .models import Profile, ProfileLog, WithdrawRequest, Bonus, BonusRequest
# Register your models here.
admin.site.register(Profile)
admin.site.register(ProfileLog)
admin.site.register(WithdrawRequest)
admin.site.register(Bonus)
admin.site.register(BonusRequest)

