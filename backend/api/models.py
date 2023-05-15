# from django.core.validators import FileExtensionValidator
# from django.contrib.auth.validators import UnicodeUsernameValidator

from Crypto.Random import random
from django.contrib.auth.models import AbstractUser
from django.db import models


def make_nonce():
    return random.randint(100000, 1000000)


def make_count():
    return random.randint(1, 5)


class User(AbstractUser):
    USERNAME_FIELD = 'wallet_address'
    date_joined = models.DateTimeField(auto_now_add=True)
    wallet_address = models.CharField(max_length=42, unique=True)
    nonce = models.CharField(max_length=6, default=make_nonce)
    rsa_privateKey = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.wallet_address


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=5)
    date = models.BigIntegerField()
    sha1 = models.CharField(max_length=40)
    file = models.BinaryField()
    network = models.TextField(blank=True, null=True)
    contract_address = models.TextField(blank=True, null=True)
    contract = models.TextField()
    result = models.JSONField(blank=True, null=True, default=dict)
    functions = models.TextField(blank=True, null=True)
    score = models.CharField(max_length=10, blank=True, null=True)
    score_ratio = models.JSONField(blank=True, null=True, default=dict)
    
    def __str__(self):
        return self.file_name


class OnlineContract(models.Model):
    class NetWork(models.TextChoices):
        bsc = "bsc"
        eth = "eth"
    
    address = models.CharField(max_length=40)
    result = models.JSONField(blank=True, null=True, default=dict)
    functions = models.TextField(blank=True, null=True)
    contract = models.TextField()


class UploadContract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.JSONField(blank=True, null=True, default=dict)
    functions = models.TextField(blank=True, null=True)
    contract = models.TextField()


class DocumentResult(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=30, blank=True, null=True)  # High / Medium / Low
    description = models.TextField(blank=True, null=True)
    details = models.JSONField(blank=True, null=True, default=dict)


class DetectionCount(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    num = models.IntegerField(default=make_count)

