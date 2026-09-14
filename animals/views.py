from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Animal


def index(request):
    """Render the main page with all animals loaded from the database."""
    animals = Animal.objects.all()
    return render(request, 'animals/index.html', {'animals': animals})


def api_search(request):
    """
    JSON endpoint used by the front-end search box.
    GET /api/search/?q=lion
    """
    query = request.GET.get('q', '').strip()

    animals = Animal.objects.all()
    if query:
        animals = animals.filter(name__icontains=query)

    data = [
        {
            'id': animal.id,
            'name': animal.name,
            'emoji': animal.emoji,
            'image_url': animal.image_url,
            'short_description': animal.short_description,
        }
        for animal in animals
    ]
    return JsonResponse({'results': data})


def api_animal_detail(request, pk):
    """
    JSON endpoint used by the "Learn More" popup.
    GET /api/animals/<id>/
    """
    animal = get_object_or_404(Animal, pk=pk)
    data = {
        'id': animal.id,
        'name': animal.name,
        'emoji': animal.emoji,
        'image_url': animal.image_url,
        'full_description': animal.full_description,
    }
    return JsonResponse(data)
