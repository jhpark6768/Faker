from django.db import models

# Create your models here.
class PhoneBook(models.Model):
    name = models.CharField(max_length=50, null=False)
    telnum = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    birth = models.DateField()

    def __str__(self):
        return self.name