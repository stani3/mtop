from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import WithdrawRequest


class SignUpForm(UserCreationForm):

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )



class WithdrawForm(forms.Form):
    address = forms.CharField(max_length=100)
    amount = forms.DecimalField(decimal_places=2, max_digits=1000)





