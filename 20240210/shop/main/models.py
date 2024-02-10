from django.db import models


class Category(models.Model):
    title = models.CharField("Название", max_length=255)

    def __str__(self):
        return self.title


class Good(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    price = models.FloatField("Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField()

    def __str__(self):
        return self.title