from django.db import models
from servicecatalog.models import ServiceProduct

class Quote(models.Model):
    quote_id = models.CharField(max_length=300, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Quote'
        ordering = ['date_added']

    def __str__(self):
        return self.quote_id

class QuoteItem(models.Model):
    service = models.ForeignKey(ServiceProduct, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)
    class Meta:
        db_table = 'QuoteItem'

    def sub_total(self):
        return self.service.service_cost * self.quantity

    def __str__(self):
        return self.service