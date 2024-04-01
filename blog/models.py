from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tegs(models.Model):
    name_tags = models.CharField(max_length=32, verbose_name="Name tegs")

    def __str__(self):
        return self.name_tags

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Post(models.Model):
    title = models.CharField(max_length=30, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Описание")
    published_date = models.DateTimeField(auto_created=True, verbose_name="Дата")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    image = models.URLField(default="http://placehold.it/900x300", verbose_name="Картинка")
    links = models.ManyToManyField(Tegs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

class Subscribe(models.Model):
    mailName = models.TextField(verbose_name="Почта")

    def __str__(self):
        return self.mailName

    class Meta:
        verbose_name = 'Почта'
        verbose_name_plural = 'Почты'


class PostPhoto(models.Model):
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(verbose_name="Картинка",upload_to="Posts_Photos")

    class Meta:
        verbose_name = 'Картинки'
        verbose_name_plural = 'Картинки'


