from django.db import models
from django.utils.text import slugify
import random
import string
from django.urls import reverse



def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(3))


class Category(models.Model):
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
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '>'.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-pickBetter" + self.name)
        super(Category, self).save(*args, **kwargs)

    #def get_absolute_url(self):
    #    return reverse("model_detail", kwargs={"pk": self.pk})


class Product(models.Model):
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
    
    #def get_absolute_url(self):
    #    return reverse("model_detail", kwargs={"pk": self.pk})
    