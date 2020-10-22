from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if username is None:
            raise TypeError("User should have a Username")
        if email is None:
            raise TypeError("User should have a Email")
        user=self.model(username=username,email=self.normalize_email(email=email))
        user.set_password(password)
        user.save()

    def create_superuser(self,username,email,password=None):
        if password is None:
            raise TypeError("Password Should not be blank")
        user=self.create_user(username=username,email=email,password=password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user