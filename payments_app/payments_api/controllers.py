import payments_app.payments_api.etherscan_api as erc20
import payments_app.payments_api.bsmartchain_api as bsc
from users.models import Bonus
from mtop_app.models import Plan
from time import sleep, time
def update_balance(wallet):
    if wallet.wlt_network == "ERC20":
        if wallet.wlt_currency == "USDT":
            balance =erc20.get_token_balance(token=erc20.USDT, address=wallet.wlt_address)
            wallet.wlt_balance = balance
        else:
            pass
    #BSC
    else:
        if wallet.wlt_currency == "USDT":
            balance = bsc.get_token_balance(token=bsc.USDT, address=wallet.wlt_address)
            wallet.wlt_balance = balance
        else:
            pass
    wallet.save()


def get_balance(wallet):
    if wallet.wlt_network == "ERC20":
        if wallet.wlt_currency == "USDT":
            balance = erc20.get_token_balance(token=erc20.USDT, address=wallet.wlt_address)
            return balance
        else:
            pass
    #BSC
    else:
        if wallet.wlt_currency == "USDT":
            balance = bsc.get_token_balance(token=bsc.USDT, address=wallet.wlt_address)
            return balance
        elif wallet.wlt_currency == "ETH":
            pass




def payment_listener(invoice, wallet):
    while True:
        wallet.wlt_free = False
        wallet.save()
        if int(time()) > invoice.timedue:
            invoice.inv_status = 5
            wallet.wlt_free = True
            invoice.save()
            wallet.save()
            return False
        balance = wallet.wlt_balance
        # works only for usdt we will see
        wbalance = get_balance(wallet)
        if wbalance >= balance + invoice.inv_price:
            invoice.inv_status = 3
            invoice.inv_paidamount = invoice.inv_price
            invoice.inv_payer.balance += invoice.inv_price
            invoice.inv_payer.plan = Plan.get_valid_plan(invoice.inv_payer.balance)
            invoice.inv_payer.save()
            invoice.save()
            wallet.wlt_balance = wbalance
            wallet.wlt_free = True
            wallet.save()
            #increment affiliate bonus commissions
            if invoice.inv_payer.referedBy is not None:
                ref = invoice.inv_payer.referedBy.profile
                ref.balance = ref.balance + ref.plan.afiliate_bonus*invoice.inv_price
                bonus = Bonus.objects.create(profile_owner=ref, amount=ref.plan.afiliate_bonus*invoice.inv_price, profile_affiliate=invoice.inv_payer)
                bonus.save()
                ref.save()
            return True
        sleep(5)