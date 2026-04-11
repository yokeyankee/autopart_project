from django.db import models
from django.utils.text import slugify

class CarBrand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название марки")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="URL-идентификатор")

    class Meta:
        verbose_name = "Марка автомобиля"
        verbose_name_plural = "Марки автомобилей"
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Автоматически генерируем slug из названия, если он не задан
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='models', verbose_name="Марка")
    name = models.CharField(max_length=100, verbose_name="Название модели")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="URL-идентификатор")

    class Meta:
        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модели автомобилей"
        ordering = ['brand__name', 'name']
        unique_together = ['brand', 'name']  # чтобы не было двух одинаковых моделей у одной марки

    def save(self, *args, **kwargs):
        if not self.slug:
            # Создаём slug вида "toyota-camry"
            self.slug = slugify(f"{self.brand.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} {self.name}"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="URL-идентификатор")

    class Meta:
        verbose_name = "Категория запчасти"
        verbose_name_plural = "Категории запчастей"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Part(models.Model):
    CONDITION_CHOICES = (
        ('new', 'Новая'),
        ('used', 'Б/У'),
    )

    article = models.CharField(max_length=50, unique=True, verbose_name="Артикул")
    name = models.CharField(max_length=200, verbose_name="Название запчасти")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    condition = models.CharField(max_length=4, choices=CONDITION_CHOICES, default='used', verbose_name="Состояние")

    # Связи с другими моделями (необязательные, т.к. запчасть может быть универсальной)
    brand = models.ForeignKey(CarBrand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Марка")
    model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Модель")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")

    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество на складе")
    image = models.ImageField(upload_to='parts/', blank=True, null=True, verbose_name="Фотография")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Запчасть"
        verbose_name_plural = "Запчасти"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.article} - {self.name}"