from django.db import models

class Payment(models.Model):
    fullname = models.CharField(max_length=100)  
    email = models.EmailField()                
    phone = models.CharField(max_length=15, default="N/A")      
    plan = models.CharField(max_length=50)     
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paystack_ref = models.CharField(max_length=15, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'Payment {self.id}'

    def get_amount(self):
        return self.amount