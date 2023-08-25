from django.shortcuts import render, redirect
from .forms import InvoiceForm
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.http import HttpResponseNotFound, HttpResponseForbidden
from .models import Invoice, Wallet
from payments_app.payments_api import controllers
from threading import Thread
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime

# Create your views here.


@login_required
def home(request):
    if request.method == 'POST':

        form = InvoiceForm(request.POST)
        if form.is_valid() and form.cleaned_data['inv_price'] >= 100:
            invoice = form.save()
            invoice.inv_payer = Profile.objects.get(user=request.user)
            wallet = Wallet.get_free_wallet(currency=invoice.inv_currency, network=invoice.inv_network)
            if wallet is not None:
                invoice.inv_wallet = wallet
            else:
                wallet = Wallet.generate_wallet(currency=invoice.inv_currency, network=invoice.inv_network)
                invoice.inv_wallet = wallet
            invoice.save()
            # assign free wallet for the invoice
            # update the balance first so we have the starting balance
            # make a listener

            controllers.update_balance(wallet)
            thread = Thread(target=controllers.payment_listener, args=(invoice, wallet,))
            thread.start()
            return redirect('payment-view', pid=invoice.inv_number)


    else:
        form = InvoiceForm()

    context = {'form': form}
    return render(request, 'payments_app/payment.html', context)


@login_required
def invoice_view(request, *args, **kwargs):
    try:
        pid = kwargs.get('pid')
        usr = Profile.objects.get(user=request.user)
        inv = Invoice.objects.get(inv_number=pid)
        context = {
            'user': usr,
            'invoice': inv,
            'wallet': inv.inv_wallet,
            'date': str(datetime.fromtimestamp(inv.inv_due))
        }
        if inv.inv_payer == usr:
            return render(request, 'payments_app/invoice_view.html', context)
        else:
            return HttpResponseForbidden("Access denied")
    except:
        return HttpResponseNotFound("invalid url")
