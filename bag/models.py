from django.db import models


class Store(models.Model):
    store_status = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.store_status
