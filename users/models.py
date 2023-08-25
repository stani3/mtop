from django.db import models
from django.contrib.auth.models import User
from time import time
from datetime import datetime
import uuid
from mtop_app.models import Plan

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    code = models.CharField(max_length=40, unique=True)
    referedBy = models.ForeignKey(User, default=None, on_delete=models.CASCADE, related_name='ref_by', null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plan, default=7, on_delete=models.CASCADE)
    @classmethod
    def generateCode(self):
        ran = str(uuid.uuid5(uuid.NAMESPACE_X500, 'c={s}'.format(s = str(uuid.uuid4())))).replace('-', '')

        return ran

    def increment_balance(self):
        self.balance = self.balance + self.balance*self.plan.intrest/100

    def __str__(self):
        return f'{ self.user.username } Profile'



class ProfileLog(models.Model):
    TYPE = [ (1, 'DEPOSIT'),
    (2, 'INTEREST'),
    (3, 'AFFILIATE'),
    (4, 'TIER CHANGE'),]
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    prev_balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    new_balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    prev_plan = models.CharField(max_length=10)
    new_plan = models.CharField(max_length=10)


    def __str__(self):
        return f'{"Date: " + str(self.date) + " " + "old balance: " + str(self.prev_balance) + " new balance: " + str(self.new_balance)}'

class WithdrawRequest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, default='')
    amount = models.DecimalField(decimal_places=2, max_digits=1000, default=0)
    date = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return f'{str(self.date) + " " + self.profile.user.username + " " + "  amount " + str(self.amount)  + "    Completed: " + str(self.completed)}'

class Bonus(models.Model):
    profile_owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    profile_affiliate = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='affiliate')
    claimed = models.BooleanField(default=False)


    def __str__(self):
        return f'{str(self.profile_owner.user.username)+ " " + "amount " + str(self.amount)  + "From: " + self.profile_affiliate.user.username}'

class BonusRequest(models.Model):
    date = models.DateTimeField(auto_now=True)
    profile_owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def get_sum(self):
        sum = 0
        bonuses = Bonus.objects.filter(profile_owner=self.profile_owner, claimed=False)
        for b in bonuses:
            sum += b.amount
        return sum
    def __str__(self):
        return f'{" Date: " + str(self.date) + " " + str(self.profile_owner.user.username)+ " " + " Approoved: " + str(self.approved)  + " amount: " + str(self.get_sum())}'

