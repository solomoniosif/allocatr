from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Allocatr.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)
    profile_photo = models.ImageField(
        verbose_name=_("profile photo"), default="https://eu2.contabostorage.com/84d43e83142241f5a2d61d2b3486c2bb:allocatr/media/profile_default.png"
    )

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name}"
            if (self.first_name and self.last_name)
            else self.username
        )
