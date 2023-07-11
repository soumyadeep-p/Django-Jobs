from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(unique = False)

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=False,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    is_recruiter = models.BooleanField(default = False)
    is_applicant = models.BooleanField(default = False)
    
    has_resume = models.BooleanField(default = False)
    has_company = models.BooleanField(default = False)

    is_verified = models.BooleanField(default=None, null=True)
    email_hash = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        unique_together = ('email', 'is_verified')