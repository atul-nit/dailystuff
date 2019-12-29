from .models import Quote, QuoteItem
from .views import _quote_id

def counter(request):
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            quote = Quote.objects.filter(quote_id=_quote_id(request))
            quote_items = QuoteItem.objects.all().filter(quote=quote[:1])
            for quote_item in quote_items:
                item_count += quote_item.quantity
        except Quote.DoesNotExist:
            item_count = 0
    return dict(item_count=item_count)