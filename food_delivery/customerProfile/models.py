from django.db import models

# Create your models here.
class CustomerProfile(Audit):
    class Meta:
        db_table = "fd_customer_profile"

    customer_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)