from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from image_cropping import ImageCropField, ImageRatioField


# Create your tags here.

class CustomPermissionManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, codename, app_label, model):
        return self.get(
            codename=codename,
            content_type=ContentType.objects.db_manager(self.db).get_by_natural_key(app_label, model),
        )


class CustomPermission(models.Model):
    name = models.CharField('Название', max_length=255)
    content_type = models.ForeignKey(
        ContentType,
        models.CASCADE,
        verbose_name='content type',
    )
    codename = models.CharField('codename', max_length=100)
    objects = CustomPermissionManager()

    class Meta:
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешения'
        unique_together = (('content_type', 'codename'),)
        ordering = ('content_type__app_label', 'content_type__model',
                    'codename')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()

    natural_key.dependencies = ['contenttypes.contenttype']


class CustomGroupManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class CustomGroup(models.Model):
    name = models.CharField('Названия', max_length=80, unique=True)
    permissions = models.ManyToManyField(
        CustomPermission,
        verbose_name='разешения',
        blank=True,
    )
    is_admin = False

    objects = CustomGroupManager()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(verbose_name='Почтовый адрес', max_length=255, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=255)
    second_name = models.CharField(verbose_name='Фамилия', max_length=255)
    avatar = ImageCropField(upload_to='avatars/', default='avatars/default-user.png',
                            verbose_name='Аватар')
    cropping = ImageRatioField('avatar', '400x400')
    date_joined = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True)
    password = models.CharField(verbose_name='Пароль', max_length=128)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'email'

    group = models.ForeignKey(
        CustomGroup,
        verbose_name='Группа',
        blank=True,
        null=True,
        help_text="Группа к которой принадлежит пользователь",
        related_name="user_set",
        related_query_name="user",
        on_delete=models.SET_NULL
    )
    user_permissions = models.ManyToManyField(
        CustomPermission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="user_set",
        related_query_name="user",
    )

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.second_name)

    def __str__(self):
        return '%s %s' % (self.first_name, self.second_name)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_admin:
            return True
        if self.group:
            if perm in [i[0] for i in list(self.group.permissions.all().values_list('codename'))]:
                return True
        return False

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = 'Аккаунт'

    def image_tag(self):  # receives the instance as an argument
        return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.avatar.url)

    image_tag.allow_tags = True
    image_tag.short_description = 'Аватар'

    def get_absolute_url(self):
        return reverse('account_edit', args=[str(self.pk)])


@receiver(pre_save, sender=Account)
def delete_old_avatars(sender, instance, raw, *args, **kwargs):
    if not raw:
        if instance.pk:
            existing_avatar = Account.objects.get(pk=instance.pk)
            if instance.avatar and existing_avatar.avatar != instance.avatar and existing_avatar.avatar.name != 'avatars/default-user.png':
                existing_avatar.avatar.delete(False)
