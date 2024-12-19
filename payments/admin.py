from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'fullname', 'email', 'phone', 'plan', 'paid', 'updated',
    ]
    list_filter = ['paid', 'created', 'updated']