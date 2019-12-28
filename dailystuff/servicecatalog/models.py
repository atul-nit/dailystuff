from django.db import models
from django.urls import reverse

class ServiceCategory(models.Model):
    category_name = models.CharField(max_length=250, unique=True)
    url_key = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='servicecategory', blank=True)

    class Meta:
        ordering = ('category_name',)
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return '{}'.format(self.category_name)

    def get_url(self):
        return reverse('servicecatalog:serviceByCategory', args=[self.url_key])

class ServiceProduct(models.Model):
    product_name = models.CharField(max_length=250, unique=True)
    url_key = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='serviceproduct', blank=True)
    servicecategory = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    service_cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    popularity = models.IntegerField(default=0)

    class Meta:
        ordering = ('product_name',)
        verbose_name = 'Service Product'
        verbose_name_plural = 'Service Products'

    def __str__(self):
        return '{}'.format(self.product_name)

    def get_url(self):
        return reverse('servicecatalog:serviceDetail',
                       args=[self.servicecategory.url_key, self.url_key])

