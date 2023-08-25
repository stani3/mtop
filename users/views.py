from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm, WithdrawForm
from django.contrib import messages
from .models import Profile, ProfileLog, WithdrawRequest, BonusRequest


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('mtop-home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('mtop-home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'users/login.html', context)


def affil(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    request.session['code'] = code
    return redirect('register-home')


def signup(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('mtop-home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                profile = Profile.objects.get(code=request.session.get('code'))
                if profile is not None:
                    r_profile = Profile.objects.get(user=user)
                    r_profile.referedBy = profile.user
                    r_profile.save()
            except:
                pass

            return redirect('mtop-home')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})





def affiliate(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        ref_users = Profile.objects.filter(referedBy=request.user)

        # if request.method == 'POST' and not BonusRequest.objects.filter(profile_owner=profile, approved=False).exists():
        #     br = BonusRequest.objects.create(profile_owner=profile)
        #     br.save()
        context = { 'code': profile.code,
                    'ref_users': ref_users,

                    }
        return render(request, 'users/affiliate.html', context)
    else:
        return redirect('mtop-home')

def profile(request):

    if request.user.is_authenticated:
        p = Profile.objects.get(user=request.user)
        context = {
            'profile': p,
        }
        return render(request, 'users/profile.html', context)
    else:
        return redirect('mtop-home')


def statistics(request):
    if request.user.is_authenticated:
        p = Profile.objects.get(user=request.user)
        lgs = ProfileLog.objects.filter(profile=p).order_by('-id')[:10]

        context = {
            'profile': p,
            'logs': lgs,
        }
        return render(request, 'users/statistics.html', context)
    else:
        return redirect('mtop-home')


def withdraw(request):
    if request.user.is_authenticated:
        p = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            form = WithdrawForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                address = form.cleaned_data['address']
                wr = WithdrawRequest.objects.create(profile=p, amount=amount, address=address)
                wr.save()
            return redirect('profile')
        else:
            form = WithdrawForm()
        context = {
            'form': form,
            'wr': WithdrawRequest.objects.filter(profile=p).order_by('-id')[:10],
            'profile': p,
        }
        return render(request, 'users/withdrawal.html', context)
