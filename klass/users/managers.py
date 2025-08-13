from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    User model manager.
    """

    def generate_username(
        self,
        clg_number: str | int,
        first_name: str,
        last_name: str,
        random_suffix: str | int | None = None,
    ) -> str:
        """
        Generates the username for the user
        The generation has 3 required parts and a 4th optional part incase we are getting a duplicate username
        - first_name by upto 12 characters, if it's less than or equal to 12 characters then the complete first_name is used, else the first 12 characters are used
        - last_name's first character
        - clg_number's last 2 digits
        - [Optional] random_suffix as a single digit number
        All parts are joined by a "."
        """
        username = ""
        if len(first_name) > 12:
            username += first_name.lower()[:12]
        else:
            username += first_name.lower()
        username += "." + last_name.lower()[:1]
        username += "." + str(clg_number)[-2:]
        if random_suffix:
            username += "." + str(random_suffix)
        return username

    def create_user(
        self,
        email,
        password,
        clg_number,
        first_name,
        last_name,
        random_suffix=None,
        **extra_fields,
    ):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        if not clg_number:
            raise ValueError(_("The College ID must be set"))
        if not first_name:
            raise ValueError(_("The First Name must be set"))
        if not last_name:
            raise ValueError(_("The Last Name must be set"))
        email = self.normalize_email(email)
        user = self.model(
            username=self.generate_username(
                clg_number, first_name, last_name, random_suffix
            ),
            email=email,
            clg_number=clg_number,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email,
        password,
        clg_number,
        first_name,
        last_name,
        random_suffix=None,
        **extra_fields,
    ):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(
            email,
            password,
            clg_number,
            first_name,
            last_name,
            random_suffix,
            **extra_fields,
        )
