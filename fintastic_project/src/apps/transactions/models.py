from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Transaction(models.Model):
    INFLOW = 'inflow'
    OUTFLOW = 'outflow'
    TYPE_CHOICES = (
        (INFLOW, _('Inflow')),
        (OUTFLOW, _('Outflow'))
    )

    reference = models.CharField(_('Reference'), max_length=64, unique=True)
    account = models.CharField(_('Account'), max_length=64)
    date = models.DateField(_('Date'))
    amount = models.DecimalField(_('Amount'), max_digits=8, decimal_places=2)
    type = models.CharField(_('Type'), max_length=16, choices=TYPE_CHOICES)
    category = models.CharField(_('Category'), max_length=32)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='transactions', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.account} - {self.reference} - {self.type} - {self.amount} - {self.category}'
