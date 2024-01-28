from django.db import models
from django.db.models.query import QuerySet
from django.utils.text import slugify
import random
import string
from django.urls import reverse


def random_slug_generator() -> str:
    """This function generates a random string of alphanumeric(ascii_letters) characters of length 3 and returns it."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))


class Category(models.Model):
    """
    A model representing a category in a store.
    """
    name = models.CharField("Категория", max_length=250, db_index=True)
    parent = models.ForeignKey("Родительсая Категория",
        'self', on_delete=models.CASCADE, related_name='children', blank=True, null=True
    )
    slug = models.SlugField("URL", max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField("Дата создания", auto_now=True)
    
    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        """Returns a string representation of the Category instance/objects.
        
        The string representation is in the form of a tree with the root category
        at the top, and each subcategory indented under its parent category. The
        full path of each category is included, with the root category's name first,
        then each parent category's name in order from root to leaf, separated by
        '>'.
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '>'.join(full_path[::-1])
    
    def save(self, *args, **kwargs) -> None:
        """Saves the current instance of the model.
        
        If the model has not been previously saved, it will be created using slugify random_slug_generator().
        If the model has been previously saved, it will be updated with the new field values provided.
        """
        if not self.slug:
            self.slug = slugify(
                random_slug_generator() + "-pickBetter" + self.name
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
    update_at = models.DateTimeField("Дата изменения", auto_now=True)

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

    This manager overrides the default manager for the Product model and provides a new method, get_queryset,
    that returns a QuerySet of all Product objects that are available. This is achieved by filtering the results
    of the default manager's get_queryset method using the available field.

    This manager can be accessed through the Product model using the objects attribute, which is a reference to the
    custom manager. For example, Product.objects.get_queryset() can be used to retrieve a QuerySet of available
    products.
    """
    def get_queryset(self) -> QuerySet:
        """Returns a QuerySet of all Product objects that are available."""
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    """
    A proxy model that provides a custom manager for the Product model.

    This proxy model inherits from the Product model and overrides the default manager
    with a custom manager that provides a new method, get_queryset, that returns a QuerySet
    of all Product objects that are available. This is achieved by filtering the results of the
    default manager's get_queryset method using the available field.

    This proxy model can be used to customize the default behavior of the Product model
    without modifying the original model class.

    Attributes:
        objects (ProductManager): The custom manager for the ProductProxy model.
    """
    objects = ProductManager.as_manager()
    
    class Meta:
        proxy = True