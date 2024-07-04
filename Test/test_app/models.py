from django.db import models
from django.utils import timezone

class CurrentUser(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField(default=100)


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(CurrentUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    market = models.CharField(default='Bit_coin', max_length=200)
    created = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()

        super().save(*args, **kwargs)

