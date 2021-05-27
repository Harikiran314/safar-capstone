from django.contrib import admin

from .models import *
admin.site.register(Account)
admin.site.register(Admin)
admin.site.register(Request)
admin.site.register(Accept)
admin.site.register(Payment)
admin.site.register(Bank_details)

