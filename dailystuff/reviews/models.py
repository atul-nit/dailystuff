from django.db import models
from servicecatalog.models import ServiceProduct


class ServiceReviews(models.Model):
    service = models.ForeignKey(ServiceProduct, on_delete=models.CASCADE)
    customer_id = models.IntegerField()
    review_comment = models.TextField(max_length=500)
    rating = models.IntegerField(default=1)
    posted_on = models.DateTimeField(auto_now_add=True)
