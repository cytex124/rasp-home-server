from django.db import models
import random


class Band(models.Model):
    choice_id = models.PositiveIntegerField()
    name = models.CharField(max_length=128)

    @staticmethod
    def get_random():
        band_pks = list(Band.objects.values_list('id', flat=True))
        pk = random.choice(band_pks)
        return Band.objects.get(pk=pk)

    class Meta:
        verbose_name = 'Band'
        verbose_name_plural = 'Bands'
        ordering = ('choice_id', 'name')

    def __str__(self):
        return '{0} - {1}'.format(self.choice_id, self.name)


class Proxy(models.Model):
    url = models.CharField(max_length=128)

    @staticmethod
    def get_random():
        proxy_pks = list(Proxy.objects.values_list('id', flat=True))
        pk = random.choice(proxy_pks)
        return Proxy.objects.get(pk=pk)

    class Meta:
        verbose_name = 'Proxy'
        verbose_name_plural = 'Proxies'
        ordering = ('url', )

    def __str__(self):
        return '{0}'.format(self.url)


class Vote(models.Model):
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE)
    bands = models.ManyToManyField(Band)
    response_code = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)
