from django.db.models import Count
from .models import Category

def categories_processor(request):
    """
    context processor to make categories available across all templates
    """
    try:
        # Convert to list to force evaluation and catch potential DB errors here
        categories = list(Category.objects.all().order_by('name'))
        return {'categories': categories}
    except Exception:
        # Return empty list if there's any issue (e.g. missing migrations)
        return {'categories': []}