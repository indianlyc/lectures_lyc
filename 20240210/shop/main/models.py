from django.db import models


class Category(models.Model):
    title = models.CharField("Название", max_length=255)

    def __str__(self):
        return self.title


def good_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / good_<id>/<filename>
    return 'good_{0}/{1}'.format(instance.id, filename)

class Good(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание")
    price = models.FloatField("Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=good_directory_path)

    def __str__(self):
        return self.title