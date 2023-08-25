from django.db import models
from time import time
from users.models import Profile
from datetime import datetime
from eth_account import Account
import secrets
import qrcode


NETWORK_TYPES = [

    ('ERC20', 'ERC20 Ethereum main'),
    ('BSC', 'Binance Smartchain(Recommended)'),
]
CURRENCY_TYPES = [
    ('USDT', 'USDT (Tether)'),
]
STATUS_TYPE = [
    (1, 'Pending Transfer'),
    (2, 'Pending Confirmation'),
    (3, 'Completed'),
    (4, 'Failed'),
    (5, 'Cancelled'),
]
class Wallet(models.Model):
    wlt_name = models.CharField(max_length=100, default='')
    wlt_balance = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    wlt_address = models.CharField(max_length=100, default='')
    wlt_network = models.CharField(max_length=10, default='BTC', choices=NETWORK_TYPES)
    wlt_currency = models.CharField(max_length=10, default='BTC', choices=CURRENCY_TYPES)
    wlt_free = models.BooleanField(default='True')
    wlt_image = models.ImageField(upload_to= 'qrs/', default=None, null=True)
    wlt_key = models.CharField(max_length=100, default='')
    def update_balance(self, amount):
        self.wlt_balance = amount

    @classmethod
    def generate_wallet(cls, network, currency):
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        acct = Account.from_key(private_key)
        address = acct.address
        img = qrcode.make(address)
        rpath = 'qrs/' + address + ".png"
        path = "media/" + rpath
        img.save(path)
        name = Wallet.objects.last().wlt_name
        name =name[:-1] + str(int(name[-1]) + 1)
        wallet = cls(wlt_name=name, wlt_balance=0, wlt_address=address, wlt_network=network, wlt_currency=currency, wlt_free=True, wlt_image=rpath, wlt_key=private_key)
        wallet.save()
        return wallet


    @classmethod
    def get_free_wallet(cls, network, currency):
        wallets = Wallet.objects.filter(wlt_currency=currency, wlt_network=network, wlt_free=True)
        if len(wallets) > 0:
            return wallets[0]
        else:
            return None

    def __str__(self):
        return f'{self.wlt_address + " " + self.wlt_name + " " + self.wlt_currency}'


class Invoice(models.Model):
    timenow = int(time())
    timedue = timenow + 1800
    inv_number = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='inv_ID')
    inv_date = models.IntegerField(default=timenow)
    inv_due = models.IntegerField(default=timedue)
    inv_status = models.IntegerField(choices=STATUS_TYPE, default=1)
    inv_price = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    inv_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, default=None, null=True)
    inv_network = models.CharField(max_length=10, default='BTC', choices=NETWORK_TYPES)
    inv_currency = models.CharField(max_length=10, default='BTC', choices=CURRENCY_TYPES)
    inv_confirmations = models.IntegerField(default='0')
    inv_paidamount = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    inv_payer = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None, null=True)

    @classmethod
    def create(cls, inv_price, inv_wallet, inv_network, inv_currency, inv_payer):
        invoice = cls(inv_price=inv_price, inv_wallet=inv_wallet, inv_network=inv_network, inv_currency=inv_currency,
                      inv_payer=inv_payer)
        # do something with the book
        return invoice

    def __str__(self):
        return f'{"Due: " + str(datetime.fromtimestamp(self.inv_due)) + " " + " " + str(self.inv_price)}'


