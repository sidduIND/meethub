from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=50)
    details = models.TextField(max_length=10000)
    venue = models.CharField(max_length=200)
    date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.')
    time = models.TimeField(help_text= 'Please use the following format: <em>HH:MM:SS<em>')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='attending', blank=True)
    num_of_attendees = models.PositiveIntegerField(default=2, blank=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['date', 'time']

    def get_absolute_url(self):
        return reverse('events:event-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def count_attendees(self):
            self.num_of_attendees = self.num_of_attendees + 1
            return self.num_of_attendees


class Comment(models.Model):
    comment = models.TextField(max_length=500)
    created_date = models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created_date', 'created_time')

    def get_absolute_url(self):
        return reverse('meet:event-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.post