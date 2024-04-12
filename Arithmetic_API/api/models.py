from django.db import models
from django.contrib.auth.models import User

class ArithmeticOperation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num1 = models.FloatField()
    num2 = models.FloatField()
    operation = models.CharField(max_length=10)
    result = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

