from .models import Category

def categories_processor(request):
    return {'footer_categories': Category.objects.all()}
