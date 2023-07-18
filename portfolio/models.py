from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.urls import path


class Subject(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics')
    edu_class = models.ForeignKey('Class', related_name='students', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar_url.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar_url.path)


class Class(models.Model):
    name = models.CharField(max_length=25, null=True)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    subjects = models.ManyToManyField(Subject, related_name='portfolios')
    profile = models.ForeignKey(Profile, related_name='portfolios', on_delete=models.CASCADE, null=True)
    main_image = models.ImageField(null=True, upload_to='images/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio-detail', kwargs={'pk': self.pk})


class Likes(models.Model):
    ip = models.CharField('IP-адрес', max_length=100)
    pos = models.ForeignKey(Portfolio, verbose_name='Публикация', on_delete=models.CASCADE)
