from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from django.core.mail import send_mail


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the system.
    username, email first_name, last_name, clg_number and password are required. Other fields are optional.
    - username is the first_name(upto the first 12 characters) + last_name(1st character) + clg_number(last 2 digits) & optional random_suffix (number) incase of duplicate issues. SEE MANAGERS.PY FOR THE FORMAT
    - clg_number is the student roll number or faculty ID
    """

    username = models.CharField(
        _("username"),
        max_length=20,
        unique=True,
        help_text=_("Required. 20 characters or fewer."),
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    clg_number = models.CharField(
        _("College ID"),
        max_length=12,
        blank=False,
        help_text="Student roll number or faculty ID",
    )
    is_faculty = models.BooleanField(
        default=False,
        null=False,
        help_text="If the user is a faculty member and thus has access to the faculty panel",
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()
    REQUIRED_FIELDS = ["clg_number", "email", "first_name", "last_name"]
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
