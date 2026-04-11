from django.contrib import admin
from .models import CarBrand, CarModel, Category, Part

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'slug')
    list_filter = ('brand',)
    prepopulated_fields = {'slug': ('name',)}  # можно использовать имя, но лучше автоматически в save
    search_fields = ('name', 'brand__name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'price', 'condition', 'brand', 'model', 'category', 'quantity')
    list_filter = ('condition', 'brand', 'category')
    search_fields = ('article', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('article', 'name', 'description', 'price', 'condition', 'quantity')
        }),
        ('Классификация', {
            'fields': ('brand', 'model', 'category')
        }),
        ('Изображение', {
            'fields': ('image',)
        }),
        ('Служебные поля', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )