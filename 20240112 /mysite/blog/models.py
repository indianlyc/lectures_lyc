from django.db import models

class Post(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст")
    datetime = models.DateTimeField("Дата и время", auto_now_add=True)