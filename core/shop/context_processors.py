from .models import Category

# type hinting imports
from django.http import HttpRequest

def categories(request: HttpRequest):
    """Retrieves all the categories that have no parent category."""
    categories = Category.objects.filter(parent=None)
    return {"categories": categories}
#filename context_processors.py