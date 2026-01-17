from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)


class Hobby(models.Model):
    class OutputType(models.TextChoices):
        PRODUCT = "P", _("Product")
        SERVICE = "S", _("Service")
        ITEM = "I", _("Item")

    output_type = models.CharField(
        max_length=1,
        choices=OutputType,
        default=OutputType.PRODUCT,
    )
    name = models.CharField(max_length=64)
    votes = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Hobby"
        verbose_name_plural = "Hobbies"


class UserHasHobby(models.Model):
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Claimed hobby"
        verbose_name_plural = "Claimed hobbies"


class Vote(models.Model):
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
