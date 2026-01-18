from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


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

    def __str__(self):
        return self.name

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
    hobby = models.ForeignKey(
        Hobby,
        related_name="votes",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

class Offering(models.Model):
    class OfferingType(models.TextChoices):
        PRODUCT = "P", _("Product")
        SERVICE = "S", _("Service")

    class StockStatus(models.TextChoices):
        IN_STOCK = "I", _("In stock")
        OUT_OF_STOCK = "O", _("Out of stock")
        MADE_ON_DEMAND = "D", _("Made on demand")


    name = models.CharField(max_length=100)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    offering_type = models.CharField(
        max_length=1,
        choices=OfferingType,
        default=OfferingType.PRODUCT,
    )
    stock_status = models.CharField(
        max_length=1,
        choices=StockStatus,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = "Offering"
        verbose_name_plural = "Offerings"
    