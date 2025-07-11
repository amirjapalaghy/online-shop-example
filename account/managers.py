from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    # def create_user(self, email, password=None, **extra_fields):

    def create_user(self, phone, password):
        if not phone:
            raise ValueError('Users must have an email address')

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):

        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
