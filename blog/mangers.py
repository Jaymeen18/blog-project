from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


from miniblog.settings import AUTH_USER_MODEL

User = AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        try:
            user = User.objects.get(email=email)

        except Exception:
            user = self.model(
                email=self.normalize_email(email)
,
                last_login=timezone.now(),
                **extra_fields
            )

            user.set_password(password)
            user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):

        user = self.create_user(email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user