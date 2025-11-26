from django.db.models import Count
from .models import Category

def categories_processor(request):
    """
    context processor to make categories available across all templates
    """
    try:
        categories = Category.objects.annotate(
            num_posts=Count('post')
        ).filter(
            num_posts__gt=0
        ).order_by('name')
        return {'categories': categories}
    except Exception as e:
        # Return empty queryset if there's any issue
        return {'categories': Category.objects.none()}