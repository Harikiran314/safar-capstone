import os
import uuid
from django.utils.timezone import now
from datetime import datetime
from django.contrib.auth.models import User

from django.db import models

class Account(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=200)

    def __str__(self):
        return str(self.fullname)


class Admin(models.Model):
    admin_username = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=False)
    admin_fullname = models.CharField(max_length=200)
    admin_phone = models.CharField(max_length=12)
    admin_email = models.CharField(max_length=200)

    def __str__(self):
        return str(self.admin_username)


def get_file_address(instance, filename):
    return '/'.join([str(instance.account_id.username),str(instance.uuid), filename])

class Request(models.Model):
    CATEGORY = (
        ('MEDICAL', 'MEDICAL'),
        ('LITERACY AND EDUCATION', 'LITERACY AND EDUCATION'),
        ('HUMAN RIGHTS', 'HUMAN RIGHTS'),
        ('PHYSICAL HELP', 'PHYSICAL HELP'),
        ('POVERTY', 'POVERTY'),
        ('OTHER', 'OTHER')
    )
    STATUS = (
        ('PENDING', 'PENDING'),
        ('ACCEPTED', 'ACCEPTED'),
        ('CANCELLED', 'CANCELLED'),
        ('COMPLETED', 'COMPLETED'),
        ('PAYMENT SUCCESSFUL', 'PAYMENT SUCCESSFUL'),
        ('PAYMENT FAILED', 'PAYMENT FAILED')
    )
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    request_category = models.CharField(max_length=50, default="OTHER", choices=CATEGORY)
    amount = models.FloatField(default=0)
    collected = models.FloatField(default=0)
    desc = models.CharField(max_length=200, default='No Description')
    identity_image = models.ImageField(upload_to=get_file_address, null=True, blank=True)
    image1 = models.ImageField(upload_to=get_file_address, null=True, blank=True)
    image2 = models.ImageField(upload_to=get_file_address, null=True, blank=True)
    deadline = models.DateField()
    status = models.CharField(max_length=50, default="PENDING", blank=True, choices=STATUS)
    pub_date = models.DateTimeField(default=now)
    admin_msg = models.CharField(max_length=200, default='none', null=True, blank=True)
    
    def __str__(self):
        return str(self.id)

    
    @property
    def remaining(self):
        rem = self.amount-self.collected
        return rem

    def percent(self):
        rem = self.collected/self.amount
        return rem*100

    @property
    def dpimage(self):
        cat = self.request_category
        if cat == 'MEDICAL':
            img = '011'
        elif cat == 'LITERACY AND EDUCATION':
            img = '022'
        elif cat == 'HUMAN RIGHTS':
            img = '033'
        elif cat == 'PHYSICAL HELP':
            img = '044'
        elif cat == 'POVERTY':
            img = '055'
        elif cat == 'OTHER':
            img = '066'
        else:
            img = '077'
        return img


    
    def image1URL(self):
        try:
            url = self.image1.url
            print(url)
        except:
            url = ''
        return url

    def image2URL(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url
    
    def identity_imageURL(self):
        try:
            url = self.identity_image.url
        except:
            url = ''
        return url
    


class Accept(models.Model):
    request_id = models.OneToOneField(Request, on_delete=models.CASCADE, null=True)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE, null=True)


class Payment(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('SUCCESSFUL', 'SUCCESSFUL'),
        ('FAILED', 'FAILED'),
    )
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    amount = models.FloatField(default=0)
    status = models.CharField(max_length=50, default="PENDING", choices=STATUS)
    date = models.DateTimeField(default=now)

class Bank_details(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    request_id = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    bank_account_no = models.CharField(max_length=20)
    bank_account_name = models.CharField(max_length=40)
    IFSC = models.CharField(max_length=20)

