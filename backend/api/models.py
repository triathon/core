# from django.core.validators import FileExtensionValidator
# from django.contrib.auth.validators import UnicodeUsernameValidator

from Crypto.Random import random
from django.contrib.auth.models import AbstractUser
from django.db import models


def make_nonce():
    return random.randint(100000, 1000000)


class User(AbstractUser):
    USERNAME_FIELD = 'wallet_address'
    date_joined = models.DateTimeField(auto_now_add=True)
    wallet_address = models.CharField(max_length=42, unique=True)
    nonce = models.CharField(max_length=6, default=make_nonce)

    def __str__(self):
        return self.wallet_address


class Document(models.Model):
    class NetWork(models.TextChoices):
        bsc = "bsc"
        eth = "eth"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=5)
    date = models.BigIntegerField()
    sha1 = models.CharField(max_length=40)
    file = models.BinaryField()
    network = models.TextField(blank=True, null=True)
    contract_address = models.TextField(blank=True, null=True)
    contract = models.TextField()
    result = models.TextField(default="{}")
    functions = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.file_name
