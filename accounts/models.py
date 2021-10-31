from django.contrib.auth.models import AbstractUser as BaseUser, UserManager as BaseUserManager


class UserManager(BaseUserManager):
    pass


class User(BaseUser):
    objects = UserManager()

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return f'{self.first_name}{self.last_name}'
