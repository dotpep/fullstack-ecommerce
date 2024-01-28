import random
import string

from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# type hinting imports
from django.db.models.query import QuerySet


def generate_random_slug() -> str:
    """This function generates a random string of alphanumeric(ascii_letters) characters of length 3 and returns it."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))


class Category(models.Model):
    """
    A model representing a category in a store.
    """
    name = models.CharField("Категория", max_length=250, db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children', blank=True, null=True
    )
    slug = models.SlugField("URL", max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField("Дата создания", auto_now=True)
    
    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        """Returns a string representation of the Category instance/objects."""
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '>'.join(full_path[::-1])
    
    def save(self, *args, **kwargs) -> None:
        """Saves the current instance of the model.
        
        If the model has not been previously saved, it will be created using slugify generate_random_slug().
        If the model has been previously saved, it will be update with the new field values provided.
        """
        if not self.slug:
            self.slug = slugify(
                generate_random_slug() + "-pickBetter" + self.name
                )
        super(Category, self).save(*args, **kwargs)

    #def get_absolute_url(self):
    #    return reverse("model_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    """
    A model representing a product in a store.
    """
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    title = models.CharField("Название", max_length=250)
    brand = models.CharField("Бренд", max_length=50)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField("URL", max_length=250)
    price = models.DecimalField("Цена", max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField("Изображение", upload_to="products/products/%Y/%m/%d")
    available = models.BooleanField("Наличие", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("model_detail", kwargs={"pk": self.pk})


class ProductManager(models.Manager):
    """
    A custom manager for the Product model that provides additional functionality.
    """
    def get_queryset(self) -> QuerySet:
        """Returns a QuerySet of all Product objects that are available."""
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    """
    A proxy model that provides a custom manager for the Product model.

    Attributes:
        objects (ProductManager): The custom manager for the ProductProxy model.
    """
    objects = ProductManager()
    
    class Meta:
        proxy = True