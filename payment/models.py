from django.db import models
from organization.models import Organization


class Payment(models.Model):
    """
    Subscription/payment record for an organization.
    One-to-one with Organization; stores billing cycle, amount, status, and dates.
    """

    BILLING_CYCLE_OPTIONS= [("month","Monthly"), ("year","Yearly")]
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    status= models.BooleanField(default=False)
    end_date= models.DateTimeField()
    cancel_at= models.DateTimeField()
    billing_cycle= models.CharField(choices=BILLING_CYCLE_OPTIONS,max_length=5)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization.name + " - " + self.amount
