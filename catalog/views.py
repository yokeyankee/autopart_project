from django.http import HttpResponse
from .models import Part

def test_parts(request):
    parts = Part.objects.all()
    output = ', '.join([p.name for p in parts])
    return HttpResponse(f"Запчасти в базе: {output}")