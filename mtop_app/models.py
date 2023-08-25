from django.db import models

# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=10, default="")
    intrest = models.DecimalField(max_digits=5, decimal_places=2)
    minimum_deposit = models.DecimalField(max_digits=1000, decimal_places=2)
    afiliate_bonus = models.DecimalField(decimal_places=2, max_digits=4, default=0.05)

    @classmethod
    def get_valid_plan(cls, balance):
        plans = Plan.objects.all().order_by('id')
        p = plans[0]
        for plan in plans:
            if balance >= plan.minimum_deposit:
                p = plan
        return p

    def __str__(self):
        return f'{str(self.name)+ " " + "intr: " + str(self.intrest)  + "% "}'


class Question(models.Model):
    question = models.CharField(max_length=100, default="")
    answer = models.TextField(max_length=20000, default="")


    def __str__(self):
        return f'{self.question + ": " + self.answer}'

class ContactRequest(models.Model):
    name = models.CharField(max_length=20, default="")
    email = models.EmailField(max_length=30, default="")
    content = models.CharField(max_length=20000, default="")
    date = models.DateTimeField(auto_now_add=True, blank=True)


    def __str__(self):
        return f'{str(self.name)+ " email: " + self.email + " :  " + self.content }'