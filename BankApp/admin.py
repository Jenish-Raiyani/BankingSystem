from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import customer,transfer_history
admin.site.register(customer)
admin.site.register(transfer_history)
