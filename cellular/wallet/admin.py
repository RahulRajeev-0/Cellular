from django.contrib import admin
from wallet.models import Wallet , WalletTransaction
# Register your models here.


admin.site.register(Wallet)
admin.site.register(WalletTransaction)