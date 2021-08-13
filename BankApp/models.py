from django.db import models

class customer(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    balance = models.FloatField()
    
    def __str__(self):
        return self.name

class transfer_history(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    sender = models.ForeignKey(customer, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(customer, on_delete=models.CASCADE, related_name='receiver')
    amount = models.FloatField()
