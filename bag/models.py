from django.db import models


class Store(models.Model):
    ''' Model to retain store status'''

    store_status = models.CharField(max_length=5)

    def __str__(self):
        return self.store_status
