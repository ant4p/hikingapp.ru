
from django.contrib.auth.models import AbstractUser
from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    UNDECIDED = 'U'
    MALE = 'M'
    FEMALE = 'F'
    ATTACK_HELICOPTER = 'H'
    GENDER_LIST = {
        'U': _('Undecided'),
        'M': _('Male'),
        'F': _('Female'),
        'H': _('Attack Helicopter'),
    }

    avatar = ThumbnailerImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True, verbose_name=_('avatar'))
    birthday = models.DateTimeField(blank=True, null=True, verbose_name=_('birthday'))
    gender = models.CharField(_('gender'), max_length=3, choices=GENDER_LIST, default=UNDECIDED)
