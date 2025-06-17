from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    # def create_user(self, email, password=None, **extra_fields):

    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None):

        user = self.create_user(
            email,
            full_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
