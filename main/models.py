from django.db import models

# Extra libraries to be imported
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, Group, PermissionsMixin)
from django.conf                import settings
from django.core.validators     import RegexValidator

class UserManager(BaseUserManager):
    def create_user_(self, email, password, role, group_name, phone, name):
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, phone=phone, name=name)
        user.set_password(password)
        user.save(using=self._db)
        Group.objects.get(name=group_name).user_set.add(user)
        return user
    
    def create_superuser(self, email, password, name, phone):
        if not email:
            raise ValueError('Email is Required.')
        if not password:
            raise ValueError('Password is Required.')
        return self.create_user_(
            email=email,
            password=password,
            role=User.SUPERUSER,
            group_name='Superuser',
            phone=phone,
            name=name
        )
    
    def create_admin(self, email, password, name, phone):
        if not email:
            raise ValueError('Email is Required.')
        if not password:
            raise ValueError('Password is Required.')
        return self.create_user_(
            email=email,
            password=password,
            role=User.ADMIN,
            group_name='Admin',
            phone=phone,
            name=name
        )
    
class User(AbstractBaseUser, PermissionsMixin):
    SUPERUSER   = 'SU'
    ADMIN       = 'AD'
    ROLE_CHOICE = (
        (SUPERUSER, 'Superuser'),
        (ADMIN, 'Admin'),
    )
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False, verbose_name='Email')
    name  = models.CharField(max_length=100, null=False, blank=False, verbose_name='Full Name')
    role  = models.CharField(max_length=2, choices=ROLE_CHOICE, default='US', verbose_name='Role')
    phone = models.CharField(validators=[RegexValidator(regex=r'^[0-9]+$', message="Without spaces, only numbers. e.g. 0167893552")], max_length=25, help_text='Without spaces, only numbers. e.g. 0167893552', null=False, blank=False, verbose_name='Phone Number')

    created_at = models.DateTimeField(verbose_name='Created At', auto_now_add=True)
    is_active  = models.BooleanField(default=True, verbose_name='Is Active')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ('id',)
        verbose_name        = 'Admin Management'
        verbose_name_plural = 'Admin Management'

    def save(self, *args, **kwargs):
        try:
            user = User.objects.get(email=self.email)
            if user.role != self.role:
                raise ValueError
            else:
                super().save(*args, **kwargs)
        except:
            super().save(*args, **kwargs)
            user = User.objects.get(email=self.email)
            for g in Group.objects.all():
                g.user_set.remove(user)
            if self.role == 'SU':
                group = 'Superuser'
            elif self.role == 'AD':
                group = 'Admin'
            Group.objects.get(name=group).user_set.add(user)
 
    @property
    def is_superuser(self):
        return self.role == 'SU'

    @property
    def is_admin(self):
        return self.role == 'AD'
    
    @property
    def is_staff(self):
        return self.is_admin or self.is_superuser
    

class ScoreAPILog(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    score      = models.CharField(max_length=8, null=True, blank=True, verbose_name='score')
    transaction_time = models.DateTimeField(verbose_name='Transaction Time', auto_now=True)

    class Meta:
        ordering = ('id',)
        verbose_name        = 'ScoreAPILog'
        verbose_name_plural = 'ScoreAPILog'

    def has_perm(self, perm, obj=None):
        return self.is_superuser and self.is_admin