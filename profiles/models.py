from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class Town(models.Model):
    """
        A profile to store town information for transport
        travel time requirements
    """

    class Meta:
        verbose_name_plural = "Towns"

    name = models.CharField(max_length=20)
    long_coord = models.DecimalField(max_digits=9, decimal_places=6)
    lat_coord = models.DecimalField(max_digits=9, decimal_places=6)

    # Will return the actual name in admin fields
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_phone_number = models.CharField(
        max_length=8, null=True, blank=True, validators=[RegexValidator(
            r'^\d{8}$', message='Incorrect number format')])
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    town = models.ForeignKey(
            'Town', null=True, blank=True, on_delete=models.SET_NULL,
            related_name='userprofile')
    default_postcode = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create and update the user profile everytime user is created
    with user info
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
