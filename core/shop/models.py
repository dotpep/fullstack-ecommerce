import random
import string

from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

# type hinting imports
from django.db.models.query import QuerySet



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
    
    @staticmethod
    def _rand_slug():
        """
        Generates a random string slug consisting of alphanumeric(ascii_letters) characters and igits of length 3 and returns it.
        
        Example:
            >>> rand_slug()
            'abc123'
        """
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
    
    
    def save(self, *args, **kwargs) -> None:
        """Saves the current instance of the model.
        
        If the model has not been previously saved, it will be created using slugify self._rand_slug().
        If the model has been previously saved, it will be update with the new field values provided.
        """
        if not self.slug:
            self.slug = slugify(
                self._rand_slug() + "-pickBetter" + self.name
                )
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category-list", args=[str(self.slug)])


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
    image = models.ImageField(
        "Изображение", upload_to="images/products/%Y/%m/%d", default='products/products/default.jfif'
    )
    available = models.BooleanField("Наличие", default=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product-detail", args=[str(self.slug)])
    
    def get_discounted_price(self):
        """
        Calculates the discounted price based on the product's price and discount.
        
        Returns:
            decimal.Decimal: The discounted price.
        """
        discounted_price = self.price - (self.price * self.discount / 100)
        return round(discounted_price, 2)

    @property
    def full_image_url(self):
        """
        Returns:
            str: The full image URL.
        """
        return self.image.url if self.image else ''



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