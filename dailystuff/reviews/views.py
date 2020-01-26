from django.shortcuts import render, get_object_or_404, redirect
from servicecatalog.models import ServiceProduct
from .models import ServiceReviews
from django.http import HttpResponse


def serviceReviews(request, service_id):
    can_add_review = True
    service = ServiceProduct.objects.get(id=service_id)
    service_reviews = ServiceReviews.objects.all().filter(service_id=service_id)
    if request.user.is_authenticated:
        customer_review = ServiceReviews.objects.all().filter(service_id=service_id, customer_id=request.user.id)
        if customer_review:
            can_add_review = False
    context = {
        'service': service,
        'service_reviews': service_reviews,
        'can_add_review': can_add_review
    }
    return render(request, 'reviews.html', context)

def addReviewRating(request, service_id):
    ratingValue = request.POST['rating']
    reviewComment = request.POST['comment']
    userId = request.POST['user_id']
    service = get_object_or_404(ServiceProduct, id=service_id)
    serviceReview = ServiceReviews.objects.create(
        service_id=service,
        customer_id=userId,
        review_comment=reviewComment,
        rating=ratingValue
    )
    serviceReview.save()
    return redirect('reviews:serviceReviews', service_id)
