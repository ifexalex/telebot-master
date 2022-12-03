from pyexpat import model
from django.db import models

class CryptoNetwork(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the network chain")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Crypto Network"
        verbose_name_plural = "Crypto Networks"


class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the cryptocurrency. eg: Bitcoin, Ethereum, Litecoin, etc.")
    symbol = models.CharField(max_length=100, help_text="Symbol of the cryptocurrency. eg: BTC, ETH, LTC, etc.")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Crypto Currency"
        verbose_name_plural = "Crypto Currencies"


class Wallets(models.Model):
    name = models.CharField(max_length=100,  help_text="Name of the wallet. eg: Bitcoin Wallet, Ethereum Wallet, Litecoin Wallet, etc.")
    address = models.CharField(max_length=100, help_text="Address of the wallet. eg: 123123123123123123123123123123123123123")
    cryptocurrency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE, related_name="cryptocurrency")
    network = models.ForeignKey(CryptoNetwork, on_delete=models.CASCADE, related_name="network", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"