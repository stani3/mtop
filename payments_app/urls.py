from django.urls import path
from . import views


urlpatterns = [
    path('deposit/', views.home, name='deposit'),
    path('payment/<int:pid>', views.invoice_view, name='payment-view'),

    ]