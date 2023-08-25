from payments_app import models
import qrcode


wallets = models.Wallet.objects.all()
for wallet in wallets:
    img = qrcode.make(wallet.wlt_address)
    rpath = 'qrs/' + wallet.wlt_address + ".png"
    path = "media/" + rpath
    img.save(path)
    wallet.wlt_image = rpath
    wallet.save()