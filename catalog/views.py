from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Part, CarBrand, CarModel, Category


def home(request):
    """Главная страница"""
    # Получаем последние добавленные запчасти
    latest_parts = Part.objects.all().order_by('-created_at')[:6]
    brands = CarBrand.objects.all()
    categories = Category.objects.all()

    context = {
        'latest_parts': latest_parts,
        'brands': brands,
        'categories': categories,
    }
    return render(request, 'catalog/home.html', context)


class PartListView(ListView):
    """Список запчастей с фильтрацией и поиском"""
    model = Part
    template_name = 'catalog/part_list.html'
    context_object_name = 'parts'
    paginate_by = 12

    def get_queryset(self):
        queryset = Part.objects.all().select_related('brand', 'model', 'category')

        # Поиск по названию или артикулу
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(article__icontains=query)
            )

        # Фильтр по марке
        brand_slug = self.request.GET.get('brand')
        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)

        # Фильтр по модели
        model_slug = self.request.GET.get('model')
        if model_slug:
            queryset = queryset.filter(model__slug=model_slug)

        # Фильтр по категории
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Фильтр по состоянию
        condition = self.request.GET.get('condition')
        if condition in ['new', 'used']:
            queryset = queryset.filter(condition=condition)

        # Фильтр по цене
        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = CarBrand.objects.all()
        context['categories'] = Category.objects.all()
        context['current_filters'] = self.request.GET.dict()
        return context


class PartDetailView(DetailView):
    """Детальная страница запчасти"""
    model = Part
    template_name = 'catalog/part_detail.html'
    context_object_name = 'part'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Похожие запчасти (той же категории)
        part = self.get_object()
        context['related_parts'] = Part.objects.filter(
            category=part.category
        ).exclude(id=part.id)[:4]
        return context